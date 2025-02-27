#!/usr/bin/env bash

set -e
shopt -s expand_aliases
source ../setup.sh

YAMLDIR="${PWD}/../examples"

OPTSTRING="d:h"
while getopts ${OPTSTRING} opt; do
  case ${opt} in
    d)
      echo "Option -d was triggered, Argument: ${OPTARG}"
      YAMLDIR="${OPTARG}"
      echo Searching for yaml files in directory $YAMLDIR
      ;;
    f)
      echo "Option -f was triggered, Argument: ${OPTARG}"
      YAMLFILE="${OPTARG}"
      echo only $YAMLFILE will be processed
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
for yamlFileWithPath in "$YAMLDIR"/*.yaml; do
    yamlFile="$(basename "$yamlFileWithPath")"
    if [[ ! -f ci-setups/"$yamlFile" ]]; then
	echo copying $yamlFileWithPath to ci-setups
	cp -f "$yamlFileWithPath" ci-setups
    fi
done

# check whether ecms.dat files are available:
for ecmsFileWithPath in "$YAMLDIR"/"ecms"*.dat; do
    ecmsFile="$(basename "$ecmsFileWithPath")"
    if [[ -f "$ecmsFileWithPath" && ! -f ci-setups/"$ecmsFile" && "$ecmsFile" != "ecms.dat" ]]; then
	echo copying $ecmsFileWithPath to ci-setups
	cp -f "$ecmsFileWithPath" ci-setups
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
    if [[ ! -f ../ecms"$filename".dat ]]; then
	k4GeneratorsConfig "../$yamlFile" --nevts 100
    else
	k4GeneratorsConfig "../$yamlFile" --ecmsFile ../ecms"$filename".dat
    fi
    cd ..
}


for yamlFile in *.yaml; do
    processYAML "$yamlFile"
done


exit 0
