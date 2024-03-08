#!/usr/bin/env bash

set -e

shopt -s expand_aliases
source ../setup.sh

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
    if [[ -e "$REFDIR/$refgenerator/$outFile" ]]; then
        if diff "$REFDIR/$refgenerator/$outFile" "$PWD/$generator/$procname/$outFile" &> /dev/null; then
            echo "Process " $procname : "Files are identical for file" $outFile 
        else
            echo "Process " $procname "Files are different for file" $outFile 
            diff "$REFDIR/$refgenerator/$outFile" "$PWD/$generator/$procname/$outFile"
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
	echo LOOKING IN $PWD/$generator
	echo LOOKING IN $generator
	ls $PWD/$generator
        for outFile in "$PWD/$generator"/*; do
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

for yamlFile in *.yaml; do
    processYAML "$yamlFile"
done

# Optionally clean up the test directory
rm -r "${CWD}/ci-setups"
exit 0
