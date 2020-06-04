import scipy.optimize as opt
import skimage.feature as skf
import random
import numpy as np 
import qim.tools as qim
import matplotlib.pyplot as plt

def plot_dual_histogram(H,xcen,ycen,markers=None,fits=None,xlabel=None,ylabel=None, **kwargs):
    Y,X = np.meshgrid(ycen,xcen,indexing='ij')
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
        xy = np.vstack((X.ravel(),Y.ravel())) #to comply with curve_fit syntax
        for p in fits:
            f = qim.gaussian2D(xy,*p)
            plt.contour(X,Y,f.reshape(H.shape),colors='r')
    plt.show()

def make_dual_histogram(xdata,ydata,nbins):
    """
    Creates a dual histogram. Wrapper of numpy.histogram2d
    Input:
        xdata: this will be on the x-axis
        ydata: this will be on the y-axis
        nbins: number of bins (the same on both axes)

    Output:
        H: Dual histogram
        xcen: Centers of bins on x axis
        ycen: Centers of bins on y axis
    """
    H,yedges,xedges = np.histogram2d(ydata.flatten(),xdata.flatten(),bins=nbins)
    xcen = (xedges[1:] + xedges[:-1])/2
    ycen = (yedges[1:] + yedges[:-1])/2

    return H, xcen, ycen

def setup_markers(H, xcen, ycen, markers=None, h=None, min_distance=20):
    """
    Creates a list of makers used as initial positions of the fitted gaussians. 
    A manual list of markers can be passed (as [[x1,y1],...,[xn,yn]]). If not the location of the peaks will be guessed from the histogram
    Input:
        H: dual histogram
        xcen: centers of bins on x-axis
        ycen: centers of bins on y-axis
    Keyword arguments:
        markers: List of marker coordinates [[x1, y1],...,[xn,yn]], default=None means automatic identification of the peaks 
        h: Threshold for h-dome filter in auto peaksearch
        min_distance: minumim distance between peaks found in auto peaksearch
    """
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
        h_dome = qim.h_dome_filter(H, h)
        ml_auto = skf.peak_local_max(h_dome, min_distance=min_distance) #gives results in row,col
        ml = [[i[1],i[0]] for i in ml_auto]

    return ml

def fit_gaussians(H,ml,xcen,ycen):
    """ 
    Fit 2D gaussians to the dual histogram.
    Input:
        H: dual histogram
        ml: marker locations
        xcen: centers of bins on x-axis
        ycen: centers of bins on y-axis
    Output:
        opts: list of fitted parameters [xc,yc,sigma_x,sigma_y,theta,amplitude,offset]
    """
    Y,X = np.meshgrid(ycen,xcen,indexing='ij') #coordinates in dual histogram
    xy = np.vstack((X.ravel(),Y.ravel())) #to comply with curve_fit syntax

    opts = []
    fitdist = H.shape[0]//10 #radius of circle to fit data within
    for m in ml:
        x0,y0 =xcen[m[0]],ycen[m[1]] 
        print('Trying to fit peak at ({:.1f}, {:.1f})'.format(x0,y0))
        Hc=H.copy()
        for i in range(Hc.shape[0]):
            for j in range(Hc.shape[1]):
                d = np.sqrt((i-m[1])**2+(j-m[0])**2)
                if d > fitdist:
                    Hc[i,j] = 0
        init = [x0,y0,1000,1000,0,H[m[1],m[0]],0]
        print('Initial guess: [{:.3f} {:.3f} {:.1f} {:.1f} {:.1f} {:1f} {:.1f}]'.format(*init))
        try:
            popt,pcov = opt.curve_fit(qim.gaussian2D,xy,Hc.ravel(),p0=init)
            print('Fitted parameters [{:.3f} {:.3f} {:.1f} {:.1f} {:.1f} {:1f} {:.1f}]'.format(*popt))
            opts.append(popt)
        except RuntimeError:
            print('Failed to fit this peak. Moving to the next.')
            continue
        print('Fitted {:d} peaks'.format(len(opts)))
    return opts

def voxel_coverage(H,xcen,ycen,opts,coverage=0.99):
    """
    Finds the minimum distance between the histogram and the fitted curves such that the given percentage of the histogram is labelled 
    Input:
        H: dual histogram
        xcen: centers of bins on x-axis
        ycen: centers of bins on y-axis
        opts: parameters for fitted curves
    Keyword arguments:
        coverage: minimum coverage of dual histogram, default=0.99
    Output:
        sigma: minimal distance threshold
    """
    phase = np.zeros(H.shape,dtype=int)
    vxlcov = 0
    sigma = 1
    while vxlcov <= coverage:
        sigma += 10**int(np.log10(sigma))
        phase = _phase_diagram(H,xcen,ycen,opts,sigma)

        vxlcov = H[phase>0].sum()/(H.sum()-H[0,0]) #subtract the background bin
        print("Finding full coverage: sigma={}, coverage={}".format(sigma,vxlcov))
    return sigma

def _phase_diagram(H,xcen,ycen,opts,sigma):
    phase = np.zeros(H.shape,dtype=int)
    for ix,x in enumerate(xcen):
        for iy,y in enumerate(ycen):
            if H[iy,ix]>0:
                distances = [qim.distance(x,y,o) for o in opts]
                i = np.argmin(distances)
                distanceMin = distances[i]
                if distanceMin < sigma:
                    phase[iy,ix] = i+1
    return phase

def phase_diagram(H,xcen,ycen,opts,sigma=None,coverage=0.99):
    """
    Labels the dual histogram
    Input:
        H: dual histogram
        xcen: centers of bins on x-axis
        ycen: centers of bins on y-axis
        opts: parameters for fitted curves
    Keyword arguments:
        coverage: minimum percentage of the histogram to label, default=0.99
        sigma: max distance to consider, default=None which means it will be computed based on the coverage
    Output:
        phasediagram: labelled dual histogram
    """
    if not sigma:
        sigma = voxel_coverage(H,xcen,ycen,opts,coverage=coverage)
    phasediagram = _phase_diagram(H,xcen,ycen,opts,sigma)
    return phasediagram

def map_to_volume(xdata, ydata, xcen, ycen, phasediagram, slicenr = None):
    """
    Assign each voxel in the volume to a label in the phase diagram.
    Inputs:
        xdata: first data volume
        ydata: seconda data volume
        xcen: centers of bins on x-axis
        ycen: centers of bins on y-axis
        phasediagram: phasediagram
    Keyword arguments:
        slicenr: if not None label only the slice with this index 
    Outputs:
        labels: labelled volume
    """
    if slicenr:
        labels = np.zeros((xdata.shape[1],xdata.shape[2]))
    else:
        labels = np.zeros(xdata.shape)
    for i, (xslice,yslice) in enumerate(zip(xdata,ydata)):
        if slicenr and i is not slicenr:
            continue
        print('Labelling slice {:d} of {:d}'.format(i,xdata.shape[0]))
        #find the bins of each pixel in the slices
        bx = np.digitize(xslice,xcen)
        by = np.digitize(yslice,ycen)
        for iy in range(xslice.shape[0]):
            for ix in range(xslice.shape[1]):
                if xdata[i,iy,ix] > 0: #this will not work if the background is not 0
                    if slicenr:
                        labels[iy,ix] = phasediagram[by[iy,ix]-1,bx[iy,ix]-1]
                    else:
                        labels[i,iy,ix] = phasediagram[by[iy,ix]-1,bx[iy,ix]-1]
    return labels