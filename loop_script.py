#! /usr/bin/env python
"""!
-----------------------------------------------------------------------------
File Name : loop_script.py

Purpose:

Created: 23-Jun-2016 07:55:30 AEST
-----------------------------------------------------------------------------
Revision History



-----------------------------------------------------------------------------
S.D.G
"""
__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = '23-Jun-2016 07:55:30 AEST'
__license__ = 'MPL v2.0'

# LICENSE DETAILS############################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# IMPORTS#####################################################################
import time
import argparse
import os
import sys
import subprocess
##############################################################################

def wall_to_int(wall):
    wall_list = [int(x) for x in wall.split(':')]

    # Check the wall list has exactly 3 elements [hours, minutes, seconds]
    assert(3 == len(wall_list))

    # Convert all to seconds and sum
    wall_total = 0
    for power, value in zip(range(len(wall_list) - 1, -1, -1), wall_list):
        wall_total += (value * (60 ** power))

    # Return the value
    return wall_total

def trigger_job_relaunch(loop_script, config_file, current_counter):
    # This function triggers to the PBS script to relaunch the job
    with open(config_file, "w") as f:
        f.write("%d" % current_counter)

    # Immediately before terminating the job, resubmit in the queue
    subprocess.call("bash %s" % loop_script)
    sys.exit(0)

def example_job(walltime, wall_lim, loop_script, config_file):

    # This function just loops and counter through the loop
    # It exemplifies how to voluntarily exit when the 
    # wall limit is approaching

    end_time = time.time() + (wall_lim * wall_to_int(walltime)) 

    # If the config_file exists load the contents
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            counter = int(f.read())
    else:
        counter = 0

    for i in range(counter, 100):
        
        # Pretend to do something 
        time.sleep(0.1)

        # Check if we have hit the wall limit
        if (end_time - time.time()) < 0:
            # Save the contents of the job and exit
            trigger_job_relaunch(loop_script, config_file, i)
    
    # If we have reached here the job has finished
    print("We are done")

    # Wrap up by deleting the config file
    os.remove(config_file) # Prevents further launching of the script


# if called from the command line
if __name__ == "__main__":

    # Define the command line arguments 
    parser = argparse.ArgumentParser(
            description = "Python loop script to test pbs script resubmission")
    parser.add_argument(
            '--walltime', '-W', '-w',
            dest='walltime',
            type=str,
            required=True, # For the purposes of this test script set to true,
                           # may not be required if wall time checking is not
                           # required
            help= \
            "The PBS format wall time for the job e.g. 00:20:00 for 20 minutes",
            )
    # Set the voluntary exit of the script
    # If set to 0.9 it will be 90% of the specified wall time
    # If time is required to save parameters keep this in mind
    # to ensure we save before hitting the wall time
    parser.add_argument(
            '--exlim', '-E', '-e',
            dest='wall_lim',
            type=float,
            help="""Percentage of wall time to execute before voluntary exit e.g
            0.9 is 90% of wall time""",
            default=0.99)
    parser.add_argument(
            '--file', '-F', '-f',
            dest='config_file',
            type=str,
            help="""The file to store the current state of the job""",
            default="jobstatus.config")
    parser.add_argument(
            '--script', '-S', '-s',
            dest='loop_script',
            type=str,
            help="""Bash script to call on voluntary exit""",
            required=True)

    options = parser.parse_args()
    example_job(**dict(options._get_kwargs()))
