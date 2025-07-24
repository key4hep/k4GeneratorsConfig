#!/usr/bin/env bash

set -e

shopt -s expand_aliases
source ../setup.sh

CWD=${PWD}
cd ci

#STEP 4
#since we have run the generators we can also do the summary now:
echo Extracting the cross sections by reading EDM4HEP files and superposing the differential distributions
eventGenerationSummary -f ${CWD}/output/GenerationSummary.dat -d ../output

exit 0
