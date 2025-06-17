#!/ usr / bin / env bash

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
    if [ -f "$file"] ; then
	cp $file ${CWD}/output/
    fi
done

cat ${CWD}/GenerationSummary.dat

echo Debugging WHizard on alma
ls -l $(CWD)/ci-setups/test-FermionProduction/Run-Cards/Whizard/Muon350/
cat $(CWD)/ci-setups/test-FermionProduction/Run-Cards/Whizard/Muon350/whizard.log

#cleanup at the end
#rm - r ${CWD } / ci - setups

        exit 0
