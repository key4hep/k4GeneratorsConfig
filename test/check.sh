#!/usr/bin/env bash

set -e

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
    local outFile="$2"
    if [[ -e "$REFDIR/$refgenerator/$outFile" ]]; then
        if diff "$REFDIR/$refgenerator/$outFile" "$PWD/$generator/$outFile" &> /dev/null; then
            echo "Files are identical."
        else
            echo "Files are different."
            diff "$REFDIR/$refgenerator/$outFile" "$PWD/$generator/$outFile"
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
    k4gen "../$yamlFile"
    checkOutputs
    cd ..
}

for yamlFile in *.yaml; do
    processYAML "$yamlFile"
done

# Optionally clean up the test directory
rm -r "${CWD}/ci-setups"
exit 0
