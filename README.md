#PBS "Auto" Submit

An example PBS submission of a python script that rather than being killed when
its walltime has exceeded voluntarily terminates and resubmits itself for
completion.

Most of the heavy lifting in this script is done within Python.  The Python
script when voluntarily terminates writes its progress status to a file
and looks for the presence of the file on relaunch.  If the file is present
it will load the contents and continue.  While this is a simple example
it can be extended to include the saving of other parameters.

Contents of this get repo:

loop.sh # The bash script that submits the PBS job
loop_script.py # The example looping job in Python

*Ensure you change the project code etc for the PBS component of 
loop.sh otherwise your job will not submit*

The mandatory arguments for loop_script.py are:
--walltime the wall time specified for the PBS job
--script the script to execute on voluntary termination
--file the filename for the progress file that gets saved along the way

By default the Python script will self terminate at 90% wall time.  This can be
changed by providing the argument
--exLim

A value of 0.99 will indicate to the script to exit at 99.9% of walltime. 
Remember to save time to save all the necessary files for early termination!


Ben Johnston 23rd June 2016

bjohnston24@gmail.com
