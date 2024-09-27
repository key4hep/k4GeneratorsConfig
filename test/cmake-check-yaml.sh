#!/usr/bin/env bash

set -e
shopt -s expand_aliases
source ../setup.sh

EXAMPLEDIR="${PWD}/../examples"

OPTSTRING="d:h"
while getopts ${OPTSTRING} opt; do
  case ${opt} in
    d)
      echo "Option -g was triggered, Argument: ${OPTARG}"
      EXAMPLEDIR="${OPTARG}"
      echo $EXAMPLEDIR is searched for
      ;;
    h)
      echo "Arguments are:" 
      echo "-h for help"
      echo "-d YAMLDIRECTORY "
      exit 0
      ;;
    ?)
      echo "Invalid option: -${OPTARG}."
      exit 1
      ;;
  esac
done

CWD=${PWD}
# only create the directory if it does not exist yet
if [[ ! -d ${CWD}/ci-setups ]]; then
   mkdir -p ${CWD}/ci-setups
else
    # clean up the content if necessary
    rm -Rf ci-setups/*
fi


# only copy if the file does not exist yet:
for yamlFileWithPath in "$EXAMPLEDIR"/*.yaml; do
    yamlFile="$(basename "$yamlFileWithPath")"
    echo checking for ci-setups/"$yamlFile"
    if [[ ! -f ci-setups/"$yamlFile" ]]; then
	echo copying $yamlFileWithPath to ci-setups
	cp -f "$yamlFileWithPath" ci-setups
    fi
done

# check whether ecms.dat files are available:
for ecmsFileWithPath in "$EXAMPLEDIR"/"ecms"*.dat; do
    ecmsFile="$(basename "$ecmsFileWithPath")"
    echo checking for "$ecmsFileWithPath"
    echo checking  ci-setups/"$ecmsFile"
    if [[ -f "$ecmsFileWithPath" && ! -f ci-setups/"$ecmsFile" && "$ecmsFile" != "ecms.dat" ]]; then
	echo copying $ecmsFileWithPath to ci-setups
	cp -f "$ecmsFileWithPath" ci-setups
    fi
done

ls -l MURKS.dat

cd ci-setups

# STEP 1: check the input

function processYAML() {
    local yamlFile="$1"
    local filename="${yamlFile%.yaml}"

    mkdir -p "test-$filename"
    cd "test-$filename"
    echo "Processing file: $yamlFile"
    if [[ ! -f ../ecms"$filename".dat ]]; then
	k4generatorsConfig -f "../$yamlFile" --nevts 100
    else
	k4generatorsConfig -f "../$yamlFile" --ecmsFile ../ecms"$filename".dat
    fi
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
