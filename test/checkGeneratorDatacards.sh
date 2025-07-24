#!/usr/bin/env bash

set -e
shopt -s expand_aliases
source ../setup.sh

EXAMPLEDIR="${PWD}/../examples"
REFDIR="${PWD}/ref-results"

OPTSTRING="g:h"
while getopts ${OPTSTRING} opt; do
  case ${opt} in
    g)
      echo "Option -g was triggered, Argument: ${OPTARG}"
      GENERATOR="${OPTARG}"
      echo $0 will only check $GENERATOR
      ;;
    h)
      echo "Arguments are:"
      echo "-h for help"
      echo "-g GENERATOR "
      exit 0
      ;;
    ?)
      echo "Invalid option: -${OPTARG}."
      exit 1
      ;;
  esac
done

CWD=${PWD}
cd ci

function checkOutputs() {
    local requestedGenerator="$1"
    if [ "$#" -eq 0 ]; then
	requestedGenerator=*
    fi
    for generator in */$requestedGenerator; do
	[[ -d "$generator" ]] || continue
	for outFile in "$PWD/$generator"/*/*; do
            [[ -f "$outFile" ]] || continue
	    local fullpath="$(dirname "$outFile")"
	    local procname="$(basename "$fullpath")"
            checkFile "$generator" "$procname" "$(basename "$outFile")"
	    # copy the files to the output
            mkdir -p "${CWD}"/output/"$generator"/"$procname"/
  	    cp "$outFile" "${CWD}"/output/"$generator"/"$procname"/"$(basename "$outFile")"
	done
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

for testDir in test-*; do
    [[ -d "$testDir" ]] || continue
    cd $testDir
    checkOutputs "$GENERATOR"
    cd ..
done


exit 0
