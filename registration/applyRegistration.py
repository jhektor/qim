import spam.DIC
import numpy as np 
import tifffile
import matplotlib.pyplot as plt

def applyRegistration(data1,data2,phi,binning,output=None, return_data=False, verbose=True):
    """
    Applies a registration defined by a spam phi-file to a dataset.
    Input:
        data1: 3D array Reference data
        data2: 3D array Data which will be registrered to the reference data. This image will be deformed.
        phi: string .tsv file defining the registration
        binning: integer    binning of the input images
        output: string  Path and filename of output image (.tif) containing the registrerd data2 array
    Keyword arguments:
        return_data: Returns registered data2 as a 3D array (default = False)
        verbose: Shows checkerboard plot of the registration (default = True)
    Output:
        Registered data2 (optional)
    """
    # Parse the phi file
    f = np.genfromtxt(phi, delimiter="\t", names=True)
    try:
        Phi = np.array([[float(f["F11"]), float(f["F12"]), float(f["F13"]), float(f['Zdisp'])],
                            [float(f["F21"]), float(f["F22"]), float(f["F23"]), float(f['Ydisp'])],
                            [float(f["F31"]), float(f["F32"]), float(f["F33"]), float(f['Xdisp'])],
                            [0, 0, 0, 1]])
    except ValueError:
        Phi = np.array([[float(f["Fzz"]), float(f["Fzy"]), float(f["Fzx"]), float(f['Zdisp'])],
                            [float(f["Fyz"]), float(f["Fyy"]), float(f["Fyx"]), float(f['Ydisp'])],
                            [float(f["Fxz"]), float(f["Fxy"]), float(f["Fxx"]), float(f['Xdisp'])],
                            [0, 0, 0, 1]])
    phibin = int(f["bin"])
    # Correct phi for different binning between the image and the phi file
    Phi[0:3,-1] *= phibin/binning

    # Apply phi to data2 image
    d2r = spam.DIC.applyPhi(data2,Phi=Phi)
    if output:
        if verbose:
            print('Saving registered tiff file')
        tifffile.imwrite(output,data=d2r.astype('uint16'))

    if verbose: #make plots
        n=3
        halfslice = data2.shape[2]//2
        cmap='Greys'
        initcheck = spam.DIC.checkerBoard(data1[:,:,halfslice],data2[:,:,halfslice],n=n)
        regcheck = spam.DIC.checkerBoard(data1[:,:,halfslice],d2r[:,:,halfslice],n=n) 

        fig,axes=plt.subplots(1,2,figsize=(16,8),sharex=True, sharey=True)
        ax = axes.ravel()
        ax[0].imshow(initcheck, cmap=cmap)
        ax[0].set_title('Before registration')
        ax[1].imshow(regcheck, cmap=cmap)
        ax[1].set_title('After registration')
        fig.tight_layout()

        initcheck = spam.DIC.checkerBoard(data1[:,halfslice,:],data2[:,halfslice,:],n=n)
        regcheck = spam.DIC.checkerBoard(data1[:,halfslice,:],d2r[:,halfslice,:],n=n) 

        fig,axes=plt.subplots(1,2,figsize=(16,8),sharex=True, sharey=True)
        ax = axes.ravel()
        ax[0].imshow(initcheck, cmap=cmap)
        ax[0].set_title('Before registration')
        ax[1].imshow(regcheck, cmap=cmap)
        ax[1].set_title('After registration')
        fig.tight_layout()

        initcheck = spam.DIC.checkerBoard(data1[halfslice],data2[halfslice],n=n)
        regcheck = spam.DIC.checkerBoard(data1[halfslice],d2r[halfslice],n=n) 

        fig,axes=plt.subplots(1,2,figsize=(16,8),sharex=True, sharey=True)
        ax = axes.ravel()
        ax[0].imshow(initcheck, cmap=cmap)
        ax[0].set_title('Before registration')
        ax[1].imshow(regcheck, cmap=cmap)
        ax[1].set_title('After registration')
        fig.tight_layout()
        plt.show()
    if return_data:
        return d2r
    