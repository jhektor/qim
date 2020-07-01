""" 
This module contains various helper functions
"""
import numpy as np
from skimage.morphology import reconstruction
import matplotlib

def find_bin_centers(edges):
    return (edges[1:] + edges[:-1])/2

def h_dome_filter(volume,h):
    seed = volume-h
    #seed = np.where(seed>0,seed,0)
    bkg = reconstruction(seed,volume,method='dilation')
    hdome = volume - bkg
    return hdome

def covariance_parameters(sx,sy,th):
    """
     Computes the elements of the inverse covariance matrix
    """
    a = np.cos(th)*np.cos(th)/(2*sx**2)+np.sin(th)*np.sin(th)/(2*sy**2)
    b = -np.sin(2*th)/(4*sx**2)+np.sin(2*th)/(4*sy**2)
    c = np.sin(th)*np.sin(th)/(2*sx**2)+np.cos(th)*np.cos(th)/(2*sy**2)
    return a,b,c

def gaussian2D(xy,x0,y0,sx,sy,th,A,of):
    (x,y)=xy #this is to comply with curve_fit
    #compute parameters https://en.wikipedia.org/wiki/Gaussian_function#Two-dimensional_Gaussian_function
    a,b,c=covariance_parameters(sx,sy,th)
    f = A*np.exp(-(a*(x-x0)**2 + 2*b*(x-x0)*(y-y0) + c*(y-y0)**2)) + of
    return f

def distance(x,y,opt): #Mahalanobis distance
    x0,y0,sx,sy,th,_,__ = opt
    a,b,c = covariance_parameters(sx,sy,th)
    return np.sqrt((a * (x - x0)**2 + 2.0 * b * (x - x0) * (y - y0) + c * (y - y0)**2))

def random_cmap(ncolors=256,startmap=None):
    """ Generate a random colormap with a specified number of colors.
        startmap is either None for random rgb values or a plt.cm object
        (e.g. plt.cm.jet) to shuffle that colormap.
        Taken from https://gist.github.com/jgomezdans/402500
    """
    if not startmap: #random rgb values
        return matplotlib.colors.ListedColormap(np.random.rand(ncolors,3))
    else:
        vals = np.linspace(0,1,ncolors)
        np.random.shuffle(vals)
        return matplotlib.colors.ListedColormap(startmap(vals))

