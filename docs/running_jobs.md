---
authors:
    - Johan Hektor
date: 2020-05-05
---
# Running jobs on Aurora
This is a short guide on how to use the job submission system on Aurora.
A more detailed explanation can be found [here](https://lunarc-documentation.readthedocs.io/en/latest/batch_system/).

## Submitting jobs
### Job script
Jobs are submitted to the cluster through a job script.
The script is a shell script (e.g. written in bash) augmented with some commands for specifying the resources needed for the job.
An example script can look like this:
```bash
#!/bin/sh
# Specify which compute project to use (only needed if user belongs to several projects)
# The name of the project can be found by running projinfo
#SBATCH -A snic2020-11-30 #This is QIM@LU

# Name of the job
#SBATCH -J test_job

# wall time of job HH:MM:SS
#SBATCH -t 00:30:00

# Ask for test queue if the job is short (max 1h and 2 nodes)
# remove one # to enable
##SBATCH --qos=test

# Number of cpus (the number of cpus is nodes*tasks-per-node
#SBATCH -N 1 #number of nodes
#SBATCH --tasks-per-node=20

# Ask for exclusive access to the node (cost is the same as for 20 cores)
# remove one # to enable
##SBATCH --exclusive

# Ask for more memory if needed (default is 3.1 GB/cpu)
# remove one # to enable
##SBATCH --mem-per-cpu=5000 #5GB/cpu

# Set name of output files (stdout and stderr).
#SBATCH -o stdout_%j.out
#SBATCH -e stderr_%j.err

# Get an email when the job is finished
#SBATCH --mail-user=johan.hektor@lunarc.lu.se
#SBATCH --mail-type=END

# Write a copy of the job script to the stdout file
cat $0

# Load the modules your program needs
module load GCC/8.3.0

# Copy input data to the compute node (optional, but might improve performance for I/O intensive jobs)
cp -p input $SNIC_TMP

# Change to execution directory (optional)
cd $SNIC_TMP

# run the program the same way as on your own computer
./program arguments

# Copy output back to submission directory (optional)
cp -p output $SLURM_SUBMIT_DIR
```
The commands starting with ```#SBATCH```are used to inform the job submission system how to handle your job.
Below the the resource specifications you put the commands needed to start your program.
It is possible to let your job access files in your home directory, however for I/O demanding jobs the performance might increase if you copy the data to a temporary directory on the compute node.
In that case you must remember to copy any output files back to your home directory before finishing the job.

### Submitting the job
Once you are happy with the job script you submit your job by running
```
sbatch name_of_job_script
```
This command will put your job in the queue and assign a job id to it.
You can monitor the progress of your jobs by running
```
squenue -u your_username
```
to cancel a job run
```
scancel job_id
```
## Interactive jobs
If you need to interact with your program while it is running (e.g. through a gui) you can ask for an interactive session on a compute node.
These sessions are also useful for code testing and debugging.
To start an interactive session with four cores on one node lasting for 60 minutes run:
```
interactive -N 1 --tasks-per-node=4 -t 60
```
Most of the options of ```SBATCH``` can also be used in the ```interactive``` command.
It is advisable to start the interactive session from a shell without any modules loaded.

## Connecting to Jupyter notebooks running on compute nodes
To be able to connect to a Jupyter notebook which is running on a compute node the following steps are needed

* Generate a Jupyter configuration file by running
```
jupyter notebook --generate-config
```
This should create a file called ```jupyter_notebook_config.py``` in ```/home/your_username/.jupyter```.

* Open the ```jupyter_notebook_config.py``` file and change the line ```#c.NotebookApp.allow_origin = ''``` to ```c.NotebookApp.allow_origin = '*'``` and the line ```#c.NotebookApp.ip = 'localhost'``` to ```c.NotebookApp.ip = '0.0.0.0'```

Make sure that the lines are uncommented (i.e. does not start with '''#''').
You'll only need to do the steps above once.
When the notebook starts it should print a link to the notebook which you can open in a browser to connect.
If you do not run an interactive session this link will be printed to the ```.out``` file of the job.
