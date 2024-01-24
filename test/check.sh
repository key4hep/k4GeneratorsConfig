#!/usr/bin/env bash

set -e

mkdir -p ci-setups

CWD=${PWD}
REFDIR="${PWD}/ref-results"
EXAMPLEDIR="${PWD}/../k4generators/examples"

cp "$EXAMPLEDIR"/*yaml ci-setups
cd ci-setups

function checkFile() {
    local generator="$1"
    local outFile="$2"
    echo Looking for file $REFDIR/$generator/$outFile
   ls -l $REFDIR/$generator/
   ls -l $REFDIR/
    if [[ -e "$REFDIR/$generator/$outFile" ]]; then
        echo "Found $outFile in reference results."
        if diff "$REFDIR/$generator/$outFile" "$PWD/$generator/$outFile" &> /dev/null; then
            echo "Files are identical."
        else
            echo "Files are different."
            diff "$REFDIR/$generator/$outFile" "$PWD/$generator/$outFile"
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
        for outFile in "$PWD/$generator"/*; do
            [[ -f "$outFile" ]] || continue
            checkFile "$generator" "$(basename "$outFile")"
        done
    done
}

function processYAML() {
    local yamlFile="$1"
    local filename="${yamlFile%.yaml}"

    mkdir -p "test-$filename"
    cd "test-$filename"
    echo "Processing file: $yamlFile"
    python3 ../../../k4generators/python/main.py -f "../$yamlFile"
    checkOutputs
    cd ..
}

for yamlFile in *.yaml; do
    processYAML "$yamlFile"
done

# Optionally clean up the test directory
rm -r "${CWD}/ci-setups"
exit 0
