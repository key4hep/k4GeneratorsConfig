#!/usr/bin/env bash

set -e

shopt -s expand_aliases
source ../setup.sh

# decode command line options

OPTSTRING=":bhr"

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
      echo "Option -f was triggered, event generation step will be run only for one process per yaml file"
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
    for generator in */*; do
        [[ -d "$generator" ]] || continue
        echo "Checking $generator"
        for outFile in "$PWD/$generator"/*/*; do
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

# STEP 1: check the input

for yamlFile in *.yaml; do
    processYAML "$yamlFile"
done

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
if [[ $runEvgen = "true" ]]; then
    counter=0
    counterRan=0
    for yamlDir in test-*; do
	cd $yamlDir
	echo $PWD is the current directory
	firstProcessRead="false"
	lastGenerator="murks"
	for aRunScript in */*/*/*.sh; do
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
	cd ..
    done
    echo k4GeneratorsConfig::EvGen Summary
    echo tried $counter generator runs
    echo with  $counterRan successful executions

    # STEP 4
    # since we have run the generators we can also do the summary now:
    echo Extracting the cross sections by reading EDM4HEP files
    $K4GENERATORSCONFIG/xsectionSummary -f ${CWD}/xsectionSummary.dat
fi

# STEP 4: clean up
rm -r "${CWD}/ci-setups"

exit 0
