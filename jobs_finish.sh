#!/bin/bash
# Script to report latest time jobs will finish on a particular HPC queue
# Ben Johnston (ben.johnston@sydney.edu.au)
# Fri Mar  3 10:08:56 AEDT 2017

if [[ $# > 0 ]]
then

    # Check for valid queue
    FOUND=0
    QUEUES=$(qstat -Q | awk '{print $1}')
    for q in $QUEUES
    do
        if [[ $q == $1 ]]
        then
            FOUND=1
            break
        fi
    done

    if [[ ${FOUND} -eq 0 ]]
    then
        echo "$1 is not a queue"
        exit
    fi 
    # Extract all of the jobs  
    JOBS=$(qstat -T | grep $1 | cut -d '.' -f 1)
    if [[ ${#JOBS[@]} -eq "0" ]]
    then
        echo "No jobs running $1"
        exit
    fi
 
    echo "Extracting all jobs for: $1"
    AVAILABLE_JOBS=$(qstat -Q | grep $1 | awk '{print $3}')
    RUNNING_JOBS=$(qstat -q | grep $1 | awk '{print $6}')
    QUEUE_JOBS=$(qstat -q | grep $1 | awk '{print $7}')

    echo "${AVAILABLE_JOBS} total available jobs"
    echo "${RUNNING_JOBS} jobs running"
    echo "${QUEUE_JOBS} jobs waiting in the queue"
    echo "Latest job finish times"

    for ID in ${JOBS}
    do
        HOURS=$(qstat -f ${ID} | grep Resource_List.walltime | cut -d '=' -f 2 | cut -d ':' -f 1)
        MINUTES=$(qstat -f ${ID} | grep Resource_List.walltime | cut -d '=' -f 2 | cut -d ':' -f 2)
        SECS=$(qstat -f ${ID} | grep Resource_List.walltime | cut -d '=' -f 2 | cut -d ':' -f 3)
        START_TIME=$(qstat -f ${ID} | grep etime | cut -d '=' -f 2)
        FINISH_TIME=$(date -d "${START_TIME} + ${HOURS} hours + ${MINUTES} min + ${SEC} sec")
        echo "Job ${ID}: ${FINISH_TIME}"
    done

else
    echo "Please enter a queue when calling the script"
    echo "e.g. bash jobs_finish.sh gpu"
fi
