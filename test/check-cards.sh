#!/usr/bin/env bash

set -e

shopt -s expand_aliases
source ../setup.sh

# decode command line options

OPTSTRING=":bhr"
generator=${1}
runEvgen="true"
runReducedEvgen="false"
while getopts ${OPTSTRING} opt; do
  case ${opt} in
#    x)
#      echo "Option -x was triggered, Argument: ${OPTARG}"
#      ;;
    b)
      echo "Option -b was triggered, event generation step will not be run"
      runEvgen="false"
      ;;
    r)
      echo "Option -r was triggered, event generation step will be run only for one process per yaml file"
      runReducedEvgen="true"
      ;;
    h)
      echo "Arguments are:" 
      echo "-h for help"
      echo "-b to block the event generation step fully"
      echo "-r to reduce the number of event generation steps to 1 per yaml file"
      exit 0
      ;;
    ?)
      echo "Invalid option: -${OPTARG}."
      exit 1
      ;;
  esac
done

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

function processYAML() {
    local yamlFile="$1"
    local filename="${yamlFile%.yaml}"

    mkdir -p "test-$filename"
    cd "test-$filename"
    echo "Processing file: $yamlFile"
    k4generatorsConfig "../$yamlFile"
    checkOutputs
    cd ..
}

# STEP 1: check the input

for yamlFile in FermionProduction.yaml; do
    processYAML "$yamlFile"
done


exit 0
