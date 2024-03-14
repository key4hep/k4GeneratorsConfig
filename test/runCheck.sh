#!/usr/bin/env bash

set -e

shopt -s expand_aliases

CWD=${PWD}

cd ci-setups

function processRun() {
    topDir=${PWD} 
    thepath="$(dirname "$1")"
    runfile="$(basename "$1")"
    echo Running $runfile in $thepath
    # move to the directory where the script is located
    cd $thepath
    # run the script
    ./$runfile
    cd $topDir
}


# now we can go through the .sh and run them
echo $PWD is the current directory
for aRunScript in */*/*/*/*.sh; do
    processRun "$aRunScript"
done

exit 0
