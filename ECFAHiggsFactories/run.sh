#!/usr/bin/env bash

# STEP 0 prepare the input

CWD=${PWD}

# STEP 2: run the generators

for runScript in */*.sh; do
    thepath="$(dirname "$runScript")"
    runfile="$(basename "$runScript")"
    cd $thepath
    echo now in $PWD
    echo Running $runfile in $thepath
    ./$runfile
    # move to the directory where the script is located
    cd $CWD
done

