import scipy.optimize as opt
import skimage.feature as skf
from skimage import filters
import random
import numpy as np 
import qim.tools as tools
import matplotlib.pyplot as plt
import multiprocessing as mp

data = None
ydata = None 
xedges = None
yedges = None
phasediagram = None
xcen = None
ycen = None

def plot_dual_histogram(H,xedges,yedges,markers=None,fits=None,xlabel=None,ylabel=None, **kwargs):
    #add one element to ycen and xcen to fix plotting issue in pcolorlabel
    #dxc = np.diff(xcen)[-1]
    #dyc = np.diff(ycen)[-1]
    #xcen = np.append(xcen,xcen[-1]+dxc)
    #ycen = np.append(ycen,ycen[-1]+dyc)
    Y,X = np.meshgrid(yedges,xedges,indexing='ij')
    plt.figure()
    plt.pcolormesh(X,Y,H,**kwargs)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    if markers:
        for m in markers:
            plt.plot(X[m[1],m[0]],Y[m[1],m[0]],'ro')
    if fits:
        #this needs the bin centers
        xc = tools.find_bin_centers(xedges)
        yc = tools.find_bin_centers(yedges)
        Y,X = np.meshgrid(yc,xc,indexing='ij')
        xy = np.vstack((X.ravel(),Y.ravel())) #to comply with curve_fit syntax
        for p in fits:
            f = tools.gaussian2D(xy,*p)
            plt.contour(X,Y,f.reshape(H.shape),colors='r')
    plt.show()

def make_dual_histogram(xdata,ydata,nbins,**kwargs):
    """
    Creates a dual histogram. Wrapper of numpy.histogram2d
    Input:
        xdata: this will be on the x-axis
        ydata: this will be on the y-axis
        nbins: number of bins (the same on both axes)

    Output:
        H: Dual histogram
        xedges: Edges of bins on x axis
        yedges: Edges of bins on y axis
    """
    H,yedges,xedges = np.histogram2d(ydata.flatten(),xdata.flatten(),bins=nbins,**kwargs)
    #xcen = xedges#(xedges[1:] + xedges[:-1])/2
    #ycen = yedges#(yedges[1:] + yedges[:-1])/2

    return H, xedges, yedges

def setup_markers(H, xedges, yedges, markers=None, h=None, min_distance=None):
    """
    Creates a list of makers used as initial positions of the fitted gaussians. 
    A manual list of markers can be passed (as [[x1,y1],...,[xn,yn]]). If not the location of the peaks will be guessed from the histogram
    Input:
        H: dual histogram
        xedges: edges of bins on x-axis
        yedges: edges of bins on y-axis
    Keyword arguments:
        markers: List of marker coordinates [[x1, y1],...,[xn,yn]], default=None means automatic identification of the peaks 
        h: Threshold for h-dome filter in auto peaksearch
        min_distance: minumim distance between peaks found in auto peaksearch, default 8% of the size of H
    """
    xcen = tools.find_bin_centers(xedges)
    ycen = tools.find_bin_centers(yedges)
    if not min_distance:
        min_distance = H.shape[0]//12
    if markers:
        ml = []
        for m in markers:
            # find bin index of current marker
            xx = np.digitize(m[0],xcen)
            yy = np.digitize(m[1],ycen)
            ml.append([xx,yy])
    else: #Automatic peak identification
        if not h:
            h = np.mean(H)
        h_dome = tools.h_dome_filter(H, h)
        h_dome = filters.median(h_dome)
        ml_auto = skf.peak_local_max(h_dome, min_distance=min_distance) #gives results in row,col
        ml = [[i[1],i[0]] for i in ml_auto]
        #remove small maximas
        ml = [m for m in ml if H[m[1],m[0]]>10]
    return ml

def fit_gaussians(H,ml,xedges,yedges,fitdist=20,mindist=10):
    """ 
    Fit 2D gaussians to the dual histogram.
    Input:
        H: dual histogram
        ml: marker locations
        xedges: centers of bins on x-axis
        yedges: centers of bins on y-axis
    Keyword arguments:
        fitdist: Radius of circle to fit data within. Scalar or list with the same number of elements as markers. default = 20
        mindist: Smallest allowed distance between two Gaussians, default = 10
    Output:
        opts: list of fitted parameters [xc,yc,sigma_x,sigma_y,theta,amplitude,offset]
    """
    xcen = tools.find_bin_centers(xedges)
    ycen = tools.find_bin_centers(yedges)
    Y,X = np.meshgrid(ycen,xcen,indexing='ij') #coordinates in dual histogram
    xy = np.vstack((X.ravel(),Y.ravel())) #to comply with curve_fit syntax
    opts = []
    
    #Sort the markers to always fit the highest first
    hv = [H[m[1],m[0]] for m in ml]
    idx = np.argsort(hv)
    ml = [ml[i] for i in idx]
    try:
        fitdist = [fitdist[i] for i in idx]
        fitdist.reverse()
    except: #fitdist wasn't a list
        pass 
    for i,m in enumerate(reversed(ml)):
        x0,y0 =xcen[m[0]],ycen[m[1]] 
        print('Trying to fit peak at ({:.1f}, {:.1f})'.format(x0,y0))
        try:
            fd = fitdist[i]
        except: #fitdist wasn't a list
            fd = fitdist
        print('Removing everything outside of {:.3f} pixels'.format(fd))
        Hc=H.copy()
        #subtract already fitted
        # if len(opts)>0:
        #     for op in opts:
        #         g = tools.gaussian2D(xy,*op)
        #         Hc -= g.reshape(Hc.shape)
        for i in range(Hc.shape[0]):
            for j in range(Hc.shape[1]):
                d = np.sqrt((i-m[1])**2+(j-m[0])**2)
                if d > fd:
                    Hc[i,j] = 0
        #check if marker is on an edge
        if (m[0]==0) or (m[0]==H.shape[0]-1) or (m[1]==0) or (m[1]==H.shape[0]-1):
            print('Marker is on an edge')
            Hc = np.zeros(H.shape)
            if (m[0]==0) or (m[0]==H.shape[0]-1): #left/right edges
                Hc[:,m[0]] = H[:,m[0]]
            elif (m[1]==0) or (m[1]==H.shape[0]-1): #bottom/top edges
                Hc[m[1],:] = H[m[1],:]
                
        # Find the amplitude and position of highest value
        idx = np.argmax(Hc)
        y0i,x0i = np.unravel_index(idx,Hc.shape)
        x0 = X[y0i,x0i]
        y0 = Y[y0i,x0i]
        H0=Hc[y0i,x0i]
        of = 0 #offset
        inits = [100,100,0]

        # Set nan and inf to 0
        Hc[~np.isfinite(Hc)]=0
        try:
            pt,pcov = opt.curve_fit(lambda xy,sx,sy,th: tools.gaussian2D(xy,x0,y0,sx,sy,th,H0,of),xy,Hc.ravel(),p0=inits)
            popt=[x0,y0,pt[0],pt[1],pt[2],H0,of]
            print('Fitted parameters [{:.3f} {:.3f} {:.3f} {:.1f} {:.1f} {:1f} {:.1f}]'.format(*popt))
            #Check if it is close to something already fitted
            if len(opts)>0:
                dist = [np.sqrt((popt[0]-op[0])**2+(popt[1]-op[1])**2) for op in opts]
                if np.min(dist)>mindist:
                    opts.append(popt)
                    print('Fitted {:d} peaks'.format(len(opts)))
                else:
                    print('This Gaussian is too close to something already fitted, d={:.3f}. Skipping.'.format(np.min(dist)))
            else:
                opts.append(popt)
                print('Fitted {:d} peaks'.format(len(opts)))
        except RuntimeError:
            print('Failed to fit this peak. Moving to the next.')
            continue
    return opts

def voxel_coverage(H,xedges,yedges,opts,coverage=0.99):
    """
    Finds the minimum distance between the histogram and the fitted curves such that the given percentage of the histogram is labelled 
    Input:
        H: dual histogram
        xedges: centers of bins on x-axis
        yedges: centers of bins on y-axis
        opts: parameters for fitted curves
    Keyword arguments:
        coverage: minimum coverage of dual histogram, default=0.99
    Output:
        sigma: minimal distance threshold
    """
    xcen = tools.find_bin_centers(xedges)
    ycen = tools.find_bin_centers(yedges)
    phase = np.zeros(H.shape,dtype=int)
    vxlcov = 0
    sigma = 1
    while vxlcov <= coverage:
        sigma += 10**int(np.log10(sigma))
        phase = _phase_diagram(H,xcen,ycen,opts,sigma)

        vxlcov = H[phase>0].sum()/(H.sum())#-H[0,0]) #subtract the background bin
        print("Finding full coverage: sigma={}, coverage={}".format(sigma,vxlcov))
    return sigma

def _phase_diagram(H,xcen,ycen,opts,sigma):
    phase = np.zeros(H.shape,dtype=int)
    for ix,x in enumerate(xcen):
        for iy,y in enumerate(ycen):
            if H[iy,ix]>0:
                distances = [tools.distance(x,y,o) for o in opts]
                i = np.argmin(distances)
                distanceMin = distances[i]
                if distanceMin < sigma: 
                    phase[iy,ix] = i+1
    return phase

def phase_diagram(H,xedges,yedges,opts,sigma=None,coverage=0.99):
    """
    Labels the dual histogram
    Input:
        H: dual histogram
        xedges: edges of bins on x-axis
        yedges: edges of bins on y-axis
        opts: parameters for fitted curves
    Keyword arguments:
        coverage: minimum percentage of the histogram to label, default=0.99
        sigma: max distance to consider, default=None which means it will be computed based on the coverage
    Output:
        phasediagram: labelled dual histogram
    """
    xcen = tools.find_bin_centers(xedges)
    ycen = tools.find_bin_centers(yedges)
    if not sigma:
        sigma = voxel_coverage(H,xcen,ycen,opts,coverage=coverage)
    phasediagram = _phase_diagram(H,xcen,ycen,opts,sigma)
    return phasediagram

def get_pdfs(xedges,yedges,opts):
    """
    Compute the probability densities of the fitted Gaussians
    """
    xcen = tools.find_bin_centers(xedges)
    ycen = tools.find_bin_centers(yedges)
    #bin size
    dx = np.diff(xcen)[0] 
    dy = np.diff(xcen)[1] 
    
    Y,X = np.meshgrid(ycen,xcen,indexing='ij') #coordinates in dual histogram
    xy = np.vstack((X.ravel(),Y.ravel())) #to comply with curve_fit syntax
    pdfs = np.zeros((len(opts),*X.shape))
    for i,op in enumerate(opts):
        sx,sy,th = op[2],op[3],op[4]
        a = np.cos(th)*np.cos(th)/(2*sx**2)+np.sin(th)*np.sin(th)/(2*sy**2)
        b = -np.sin(2*th)/(4*sx**2)+np.sin(2*th)/(4*sy**2)
        c = np.sin(th)*np.sin(th)/(2*sx**2)+np.cos(th)*np.cos(th)/(2*sy**2)
        Si = np.array([[a,b],[b,c]]) #Inverse covariance matrix
        S = np.linalg.inv(Si)
        detS = np.linalg.det(S)
        mu = np.array([op[0],op[1]])
        pdf = np.zeros(xy.shape[1])
        for k,phi in enumerate(xy.T):
            pdf[k] = 1./(2*np.pi*np.sqrt(detS))*np.exp(-0.5*(np.dot(phi-mu,np.dot(Si,phi-mu))))*dx*dy
        pdfs[i]=pdf.reshape(X.shape)
    return pdfs



def map_to_volume(xdatain, ydatain, xedgesin, yedgesin, phasediagramin, slicenr = None, slicedir=0,nprocs=1):
    """
    Assign each voxel in the volume to a label in the phase diagram.
    Inputs:
        xdata: first data volume
        ydata: seconda data volume
        xedges: edges of bins on x-axis
        yedges: edges of bins on y-axis
        phasediagram: phasediagram
    Keyword arguments:
        slicenr: if not None label only the slice with this index 
        slicedir: axis to slice in (0,1,2)
    Outputs:
        labels: labelled volume
    """
    global xdata
    global ydata
    global xedges
    global yedges
    global phasediagram
    global xcen
    global ycen
    xdata = xdatain
    ydata = ydatain
    xedges = xedgesin
    yedges = yedgesin
    phasediagram = phasediagramin

    xcen = tools.find_bin_centers(xedges)
    ycen = tools.find_bin_centers(yedges)
    if slicenr:
        if slicedir == 0:
            labels = np.zeros((xdata.shape[1],xdata.shape[2]))
            xs = xdata[slicenr]
            ys = ydata[slicenr]
        elif slicedir == 1:
            labels = np.zeros((xdata.shape[0],xdata.shape[2]))
            xs = xdata[:,slicenr,:]
            ys = ydata[:,slicenr,:]
        elif slicedir == 2:
            labels = np.zeros((xdata.shape[0],xdata.shape[1]))
            xs = xdata[:,:,slicenr]
            ys = ydata[:,:,slicenr]
        bx = np.digitize(xs,xcen)
        by = np.digitize(ys,ycen)   
        for iy in range(xs.shape[0]):
            for ix in range(xs.shape[1]):
                labels[iy,ix] = phasediagram[by[iy,ix]-1,bx[iy,ix]-1]     
    else:
        #labels = np.zeros(xdata.shape)
        a=list(range(0,xdata.shape[0]+xdata.shape[0]//nprocs, xdata.shape[0]//nprocs))
        arguments = [[a[i],a[i+1]] for i in range(len(a)-1)]
        print('Setting up pool with {:d} processors'.format(nprocs))
        with mp.Pool( nprocs ) as p:
            labels = p.map( _map_parallel, arguments)
        labels=np.concatenate(labels)
    return labels

def _map_parallel(arguments):
    xdata_sliced = xdata[arguments[0]:arguments[1]]
    ydata_sliced = ydata[arguments[0]:arguments[1]]  
    labels = np.zeros(xdata_sliced.shape)
    for i, (xslice,yslice) in enumerate(zip(xdata_sliced,ydata_sliced)):
        #find the bins of each pixel in the slices
        bx = np.digitize(xslice,xcen)
        by = np.digitize(yslice,ycen)
        for iy in range(xslice.shape[0]):
            for ix in range(xslice.shape[1]):
                labels[i,iy,ix] = phasediagram[by[iy,ix]-1,bx[iy,ix]-1]
    return labels

