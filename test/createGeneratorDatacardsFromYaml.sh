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
if [[ ! -d ${CWD}/ci ]]; then
   mkdir -p ${CWD}/ci
else
    # clean up the content if necessary
    rm -Rf ci/*
fi
# only create the directory if it does not exist yet
if [[ ! -d ${CWD}/output ]]; then
   mkdir -p ${CWD}/output
else
    # clean up the content if necessary
    rm -Rf output/*
fi


# only copy if the file does not exist yet:
for yamlFileWithPath in "$YAMLDIR"/*.yaml; do
    yamlFile="$(basename "$yamlFileWithPath")"
    if [[ ! -f ci/"$yamlFile" ]]; then
	echo copying $yamlFileWithPath to ci
	cp -f "$yamlFileWithPath" ci
    fi
done

# check whether ecms.dat files are available:
for ecmsFileWithPath in "$YAMLDIR"/"ecms"*.dat; do
    ecmsFile="$(basename "$ecmsFileWithPath")"
    if [[ -f "$ecmsFileWithPath" && ! -f ci/"$ecmsFile" && "$ecmsFile" != "ecms.dat" ]]; then
	echo copying $ecmsFileWithPath to ci
	cp -f "$ecmsFileWithPath" ci
    fi
done

cd ci

# STEP 1: check the input

function processYAML() {
    local yamlFile="$1"
    local filename="${yamlFile%.yaml}"

    mkdir -p "test-$filename"
    cd "test-$filename"
    echo "Processing file: $yamlFile"
    if [[ ! -f ../ecms"$filename".dat ]]; then
	k4GeneratorsConfig "../$yamlFile"
    else
	k4GeneratorsConfig "../$yamlFile" --ecmsFile ../ecms"$filename".dat
    fi
    cd ..
}


for yamlFile in *.yaml; do
    processYAML "$yamlFile"
done


exit 0
