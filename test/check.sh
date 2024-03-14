#!/usr/bin/env bash

set -e

shopt -s expand_aliases
source ../setup.sh

# STEP 0 prepare the input

mkdir -p ci-setups

CWD=${PWD}
REFDIR="${PWD}/ref-results"
EXAMPLEDIR="${PWD}/../examples"

cp "$EXAMPLEDIR"/*yaml ci-setups
cd ci-setups

function checkFile() {
    local generator="$1"
    local refgenerator="$(basename "$generator")"
    local procname="$2"
    local outFile="$3"
    if [[ -e "$REFDIR/$refgenerator/$procname/$outFile" ]]; then
        if diff "$REFDIR/$refgenerator/$procname/$outFile" "$PWD/$generator/$procname/$outFile" &> /dev/null; then
            echo "Process " $procname : "Files are identical for file" $outFile 
        else
            echo "Process " $procname "Files are different for file" $outFile 
            diff "$REFDIR/$refgenerator/$procname/$outFile" "$PWD/$generator/$procname/$outFile"
            exit 1
        fi
    else
        echo "Did not find $outFile. Not checking!"
    fi
}

function checkOutputs() {
    for generator in */*; do
        [[ -d "$generator" ]] || continue
        echo "Checking $generator"
        for outFile in "$PWD/$generator"/*/*; do
            [[ -f "$outFile" ]] || continue
	    local fullpath="$(dirname "$outFile")"
	    local procname="$(basename "$fullpath")"
            checkFile "$generator" "$procname" "$(basename "$outFile")"
        done
    done
}

function processYAML() {
    local yamlFile="$1"
    local filename="${yamlFile%.yaml}"

    mkdir -p "test-$filename"
    cd "test-$filename"
    echo "Processing file: $yamlFile"
    k4gen -f "../$yamlFile"
    checkOutputs
    cd ..
}

# STEP 1: check the input

for yamlFile in *.yaml; do
    processYAML "$yamlFile"
done

# STEP 2: run the generators

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


# STEP 3: clean up
rm -r "${CWD}/ci-setups"

exit 0
