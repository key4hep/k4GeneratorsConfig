#!/usr/bin/env bash

set -e
shopt -s expand_aliases
source ../setup.sh

CWD=${PWD}
# only create the directory if it does not exist yet
if [[ ! -d ${CWD}/ci-setups ]]; then
   mkdir -p ${CWD}/ci-setups
else
    # clean up the content if necessary
    rm -Rf ci-setups/*
fi

EXAMPLEDIR="${PWD}/../examples"

# only copy if the file does not exist yet:
for yamlFileWithPath in "$EXAMPLEDIR"/FermionProduction.*yaml; do
   yamlFile="$(basename "$yamlFileWithPath")"
   echo checking for ci-setups/"$yamlFile"
   if [[ ! -f ci-setups/"$yamlFile" ]]; then
      echo copying $yamlFileWithPath to ci-setups
      cp -f "$yamlFileWithPath" ci-setups
   fi
done

cd ci-setups

# STEP 1: check the input

function processYAML() {
    local yamlFile="$1"
    local filename="${yamlFile%.yaml}"

    mkdir -p "test-$filename"
    cd "test-$filename"
    echo "Processing file: $yamlFile"
    k4gen -f "../$yamlFile" --nevts 100
    checkOutputs
    cd ..
}

function checkOutputs() {
    # for generator in */*; do
    # if [[ -d "$generator" ]] || continue
    echo "Checking $generator"
    for outFile in "$PWD/$generator"/*/*; do
        [[ -f "$outFile" ]] || continue
    local fullpath="$(dirname "$outFile")"
    local procname="$(basename "$fullpath")"
        checkFile "$generator" "$procname" "$(basename "$outFile")"
        # done
    done
}

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

for yamlFile in *.yaml; do
    processYAML "$yamlFile"
done


exit 0
