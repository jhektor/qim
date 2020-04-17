# Getting started with image analysis on LUNARC
## Cloning the git repository
The code developed in the QIM project is hosted on GitHub [here](https://github.com/jhektor/qim).
To get the code you can either download a snapshot of the repository, or clone it.
To clone the repository run
```
git clone https://github.com/jhektor/qim.git
```
in a terminal.
This will create a local copy of the repository in a folder called qim in the current directory.
To sync your local copy with the GitHub repository run
```
git pull
```
inside the qim directory.
If you have modified any files in your local repository the `git pull` command will likely give a bunch of error messages.
A bette approach in case you want to modify the code is to fork the GitHub repository.
To set-up the forked repository you can follow [this](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) tutorial.
If you have improved on the code or implemented a new feature you are very welcome to create a pull request to add your code to the qim repository.
You can read about how to do that [here](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork).

## Python environments
### A short guide to Conda
We use Conda for managing the python environments used for different python-based software on LUNARC.
Conda is part of the Anaconda Python distribution, which on LUNARC is activated by running
```
module load anaconda3
```
in a terminal.
This will load the Python 3 version of Anaconda, there is also a Python 2 version available (`module load anaconda2`).
You can now list all available Conda environments with
```
conda info -e
```
The currently active environment is marked with `*`.
To change to a different environment run
```
source activate NAME
```
where `NAME` is the name of the environment you want to use.
The environment will only be active in the terminal you issue the command in.
If you want to use multiple terminal windows you'll need to activate the environment in all of them, after loading the anaconda module.

You can create a new environment with a specific version of python with e.g.
```
conda create -n NAME pyton=3.7
```
You can install packages with
```
conda install -n NAME PACKAGE_1 PACKAGE_2
```
where NAME is the name of the environment to install the package in, if you do not include the `-n` keyword the package will be installed in the currently active environment.
You can install multiple packages at the same time.
To remove a package from an environment use
```
conda remove --name NAME PACKAGE
```
and to remove the whole environment
```
conda remove --n NAME --all
```

It is also possible to install environments defined in a configuration file.
This is the easiest way to install the environments for image analysis and will be used to install the environments described below.
The installation is done using
```
conda env create -f CONFIG.yml
```
where CONFIG.yml is the file defining the environment.

### Available python environments
#### QIM
This is the standard environment for the code developed in the QIM project.
It contains the standard anaconda3 packages as well as [jupyterlab](https://jupyterlab.readthedocs.io/en/stable/) (for running jupyter notebooks), [dxchange](https://dxchange.readthedocs.io/en/latest/) (for reading data), and [scikit-image](https://scikit-image.org) (for image processing).
This environment is installed by running
```
conda env create -f envs/qim_env.yml
```
from the qim directory and is activated by
```
module load anaconda3
source activate qim
```

#### Tomopy
[Tomopy](https://tomopy.readthedocs.io/en/latest/) is an open-source Python package for reconstruction of tomographic data from, mainly, synchrotrons.
The Python environment for Tomopy is created by running
```
conda env create -f envs/tomopy_env.yml
```
and activate by
```
module load anaconda3
source activate tomopy
```
