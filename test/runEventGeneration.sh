#!/usr/bin/env bash

set -e

shopt -s expand_aliases
source ../setup.sh

# decode command line options

OPTSTRING="g:h"
GENERATOR=""
while getopts ${OPTSTRING} opt; do
  case ${opt} in
    g)
      echo "Option -g was triggered, event generation step will be run only for ${OPTARG}"
      GENERATOR="$OPTARG"
      ;;
    h)
      echo "Arguments are:" 
      echo "-h for help"
      echo "-g GENERATORNAME only run this generator"
      exit 0
      ;;
    ?)
      echo "Invalid option: -${OPTARG}."
      exit 1
      ;;
  esac
done

# if the generator is not requested explicitely, we define a wildcard (=all)
if [ -z $GENERATOR ]; then
    GENERATOR=*
fi

CWD=${PWD}
cd ci-setups

# run a generator: argument is a pathname
function processRun() {
    topDir=${PWD} 
    thepath="$(dirname "$1")"
    runfile="$(basename "$1")"
    echo Running $runfile in $thepath
    # move to the directory where the script is located
    cd $thepath
    # run the script
    ./$runfile
    if [[ $? -eq 0 ]]; then
	echo k4GeneratorsConfig::Event generation successful for $runfile in directory $thepath
    fi
    cd $topDir
}

# loop through all directors to run all files
for yamlDir in test-*; do
    cd $yamlDir
    file_pattern="*/${GENERATOR}/*/*.sh"
    if ls $file_pattern 1> /dev/null 2>&1; then
    	for aRunScript in ${file_pattern}; do
    	    processRun "$aRunScript"
    	done
    fi
    cd ..
done

exit 0
