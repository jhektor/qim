# qim
Image analysis scripts developed under the QIM project at Lund University. Members of the QIM project can import the code on LUNARC with 
```
sys.path.insert(0, '/lunarc/nobackup/projects/qim')
```


## Contents
### docs
The documentation on how to use the LUNARC clusters can be found [here](https://qimlu.readthedocs.io/en/latest/)

### scripts
#### mergeTiffs
Script for merging a stack of tif files to a single file
#### readVol.py
Convert .vol files (from ID19 (?)) to .tif
#### txmViewer.py
Python script to read and plot data from txm files. 
#### txm2tiff
Script for converting txm files to tif

### notebooks
#### data_summary.ipynb
Jupyter notebook producing a quick overview of some data
#### foam_ex.ipynb
Jupyter notebook illustrating segmentation and basic quantification of 3D data.
#### segmentation_v2.ipynb
Jupyter notebook illustrating how to use the registration module to segment based on a dual histogram

## Modules
### inout
Tools for reading and converting between data formats
### registration
Module for registering two volumes and doing segmentation based on the dual histogram.
### tools
Various small helper functions.

### envs
.yml files for setting up python environments on Aurora. Not very useful any longer.
