# qim
Image analysis scripts developed under the QIM project at Lund University


## Contents
### scripts
#### txmViewer.py
Python script to read and plot data from txm files. 
##### Requirements
* dxchange https://dxchange.readthedocs.io/en/latest/
#### readVol.py
Convert .vol files (from ID19 (?)) to .tif

### notebooks
#### foam_ex.ipynb
Jupyter notebook illustrating segmentation and basic quantification of 3D data.
##### Requirements
* dxchange https://dxchange.readthedocs.io/en/latest/

### registration
Module for registering two volumes and doing segmentation based on the dual histogram.
#### Requirements
* spam https://ttk.gricad-pages.univ-grenoble-alpes.fr/spam/index.html

### envs
.yml files for setting up python environments on Aurora

### docs
The documentation on how to use the LUNARC clusters can be found [here](https://qimlu.readthedocs.io/en/latest/)
