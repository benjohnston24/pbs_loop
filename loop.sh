#! /bin/bash
# This script provides one example of how to automatically resubmit a job to
# PBS until it has completed its task irrespective of walltime.  
# This example uses a simple python script to simulate the job that
# upon getting close to the walltime voluntarily terminates early saving its
# progress to a configuration file.  
# The python script then recalls this job submission script prior to
# terminating

# Ben Johnston
# 23rd June 2016

WALLTIME=00:00:10
CONFIG_FILE=job_status.config
THIS_SCRIPT=`basename "$0"`

cat << EOF | qsub 

#PBS -P predPap
#PBS -N loopDemo
#PBS -l nodes=1:ppn=1
#PBS -l walltime=${WALLTIME}
#PBS -l mem=1kb
#PBS -q defaultQ

# Load modules
module load python

# Change directory
cd \$PBS_O_WORKDIR

# Execute the python script
python loop_script.py --walltime $WALLTIME --file $CONFIG_FILE --script \$PBS_O_WORKDIR/$THIS_SCRIPT

EOF
