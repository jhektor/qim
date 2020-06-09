""" 
This module contains various helper functions
"""
import numpy as np
from skimage.morphology import reconstruction


def h_dome_filter(volume,h):
    seed = volume-h
    #seed = np.where(seed>0,seed,0)
    bkg = reconstruction(seed,volume,method='dilation')
    hdome = volume - bkg
    return hdome

def gaussian2D(xy,x0,y0,sx,sy,th,A,of):
    (x,y)=xy #this is to comply with curve_fit
    #compute parameters https://en.wikipedia.org/wiki/Gaussian_function#Two-dimensional_Gaussian_function
    a = np.cos(th)*np.cos(th)/(2*sx**2)+np.sin(th)*np.sin(th)/(2*sy**2)
    b = -np.sin(2*th)/(4*sx**2)+np.sin(2*th)/(4*sy**2)
    c = np.sin(th)*np.sin(th)/(2*sx**2)+np.cos(th)*np.cos(th)/(2*sy**2)
    f = A*np.exp(-(a*(x-x0)**2 + 2*b*(x-x0)*(y-y0) + c*(y-y0)**2)) + of
    return f

def distance(x,y,opt): #Mahalanobis distance
    x0,y0,sx,sy,th,_,__ = opt
    a = np.cos(th)*np.cos(th)/(2*sx**2)+np.sin(th)*np.sin(th)/(2*sy**2)
    b = -np.sin(2*th)/(4*sx**2)+np.sin(2*th)/(4*sy**2)
    c = np.sin(th)*np.sin(th)/(2*sx**2)+np.cos(th)*np.cos(th)/(2*sy**2)
    return np.sqrt((a * (x - x0)**2 + 2.0 * b * (x - x0) * (y - y0) + c * (y - y0)**2))
