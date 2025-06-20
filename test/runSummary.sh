#!/usr/bin/env bash

set -e

shopt -s expand_aliases
source ../setup.sh

CWD=${PWD}
cd ci-setups

#STEP 4
#since we have run the generators we can also do the summary now:
echo Extracting the cross sections by reading EDM4HEP files and superposing the differential distributions
$K4GENERATORSCONFIG/eventGenerationSummary -f ${CWD}/GenerationSummary.dat

for file in *.png *.pdf *.root; do
    echo FOUND file $file >> ${CWD}/GenerationSummary.dat
    if [ -f "$file" ]; then
	cp $file ${CWD}/output/
	echo COPIED file $file to ${CWD}/output >> ${CWD}/GenerationSummary.dat
    fi
done

exit 0
