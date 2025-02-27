#!/usr/bin/env bash

set -e

shopt -s expand_aliases
source ../setup.sh

# decode command line options

OPTSTRING="g:hr"
runReducedEvgen="false"
GENERATOR=""
while getopts ${OPTSTRING} opt; do
  case ${opt} in
    r)
      echo "Option -r was triggered, event generation step will be run only for one process per yaml file"
      runReducedEvgen="true"
      ;;
    g)
      echo "Option -g was triggered, event generation step will be run only ${optarg}"
      GENERATOR="$optarg"
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


CWD=${PWD}
REFDIR="${PWD}/ref-results"
EXAMPLEDIR="${PWD}/../examples"
cd ci-setups

# STEP 2: run the generators

function processRun() {
    isOK=0
    topDir=${PWD} 
    thepath="$(dirname "$1")"
    runfile="$(basename "$1")"
    echo Running $runfile in $thepath
    # move to the directory where the script is located
    cd $thepath
    # run the script
    k4ConfigRanGen=0
    ./$runfile
    if [[ $? -eq 0 ]]; then
	echo k4GeneratorsConfig::Event generation succssful for $runfile in directory $thepath
	k4ConfigRanGen=1
    else
	k4ConfigRanGen=0
    fi
    cd $topDir
}

# STEP 3 now we can go through the .sh and run them
counter=0
counterRan=0
for yamlDir in test-*; do
    cd $yamlDir
    echo $PWD is the current directory
    firstProcessRead="false"
    lastGenerator="murks"
    file_pattern="*/${GENERATOR}/*/*.sh"
    if ls $file_pattern 1> /dev/null 2>&1; then
    	for aRunScript in ${file_pattern}; do
    	    proc="$(dirname "$aRunScript")"
    	    generatorWithPath="$(dirname "$proc")"
    	    if [[ $runReducedEvgen = "true" && $firstProcessRead = "true" && $generatorWithPath = "$lastGenerator" ]]; then
    		continue
    	    fi
    	    firstProcessRead="true"
    	    lastGenerator=$generatorWithPath
    	    if [[ $k4ConfigRanGen -eq 1 ]]; then
    		counterRan=$((counterRan+1))
    	    fi
    	    counter=$((counter+1))
    	    processRun "$aRunScript"
    	done
    else
        echo "No executables for this generator, continuing"
        counter=$((counter+1))    
        counterRan=$((counterRan+1))
    fi
    cd ..
done
echo k4GeneratorsConfig::EvGen Summary
echo tried $counter generator runs
echo with  $counterRan successful executions

exit 0
