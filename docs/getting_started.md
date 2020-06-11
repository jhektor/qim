---
authors:
    - Johan Hektor
date: 2020-06-09
---
# Getting started with image analysis on LUNARC
## The essentials
This is a very quick guide to getting started with the LUNARC system.
A more detailed version is found below.
### Connect to Aurora
Either connect to the HPC desktop as described [here](https://lunarc-documentation.readthedocs.io/en/latest/using_hpc_desktop/) or ssh to `aurora.lunarc.lu.se`

### Enable the QIM software environment
Enable the QIM virtual environment
```
source /lunarc/nobackup/projects/qim/load_qim_env.sh
```

### Running code
Python scripts
```
python script.py arguments -keywords
```
Jupyter notebooks
```
jupyter lab notebook.ipynb
```
open the link printed in the terminal with a browser (e.g. Firefox) to access the notebook.

### Transfer data from your local computer
```
scp file your_username@aurora.lunarc.lu.se:/home/your_username/
```

## More details
### QIM software environment
A description will be here soon.

#### Cloning the git repository
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
A better approach in case you want to modify the code is to fork the GitHub repository.
To set-up the forked repository you can follow [this](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) tutorial.
If you have improved on the code or implemented a new feature you are very welcome to create a pull request to add your code to the qim repository.
You can read about how to do that [here](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork).

### Transferring data to LUNARC
At the moment the most convenient way to transfer data to and from LUNARC is to use ´scp´ in a terminal.
To transfer a file from your local computer to your `/home` directory on Aurora the syntax is
```
scp file your_username@aurora.lunarc.lu.se:/home/your_username/
```
You'll then need to input your password and a Pocket Pass OTP in the terminal.
You can find more examples on how to use scp [here](http://www.hypexr.org/linux_scp_help.php).
The path to the folder for the QIM storage project on Aurora is `/lunarc/nobackup/projects/qim`.
There should also be a soft-link to the folder in your home directory.
Each of the projects in QIM are given a separate folder within the storage folder.
