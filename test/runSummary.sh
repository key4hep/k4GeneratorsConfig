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
    if [ -f "$file"] ; then
	cp $file ${CWD}/output/
    fi
done

cat ${CWD}/GenerationSummary.dat

echo Debugging WHizard on alma
ls -l ${CWD}/ci-setups/test-FermionProduction/Run-Cards/Whizard/Muon350/ >> ${CWD}/GenerationSummary.dat
cat ${CWD}/ci-setups/test-FermionProduction/Run-Cards/Whizard/Muon350/whizard.log >> ${CWD}/GenerationSummary.dat
echo " "
echo ls /cvmfs/sw-nightlies.hsf.org/key4hep/releases/2025-06-07/x86_64-almalinux9-gcc14.2.0-opt/whizard/3.1.5-3v5fcx/lib/libomega.so.0.0.0
ls -l /cvmfs/sw-nightlies.hsf.org/key4hep/releases/2025-06-07/x86_64-almalinux9-gcc14.2.0-opt/whizard/3.1.5-3v5fcx/lib/libomega.so.0.0.0 >> ${CWD}/GenerationSummary.dat
ls -l /cvmfs/sw-nightlies.hsf.org/key4hep/releases/2025-06-07/x86_64-almalinux9-gcc14.2.0-opt/whizard/3.1.5-3v5fcx/lib/* >> ${CWD}/GenerationSummary.dat
echo " "
echo COmpiler listing:
cat ${CWD}/ci-setups/test-FermionProduction/Run-Cards/Whizard/Muon350/default_lib.makefile >> ${CWD}/GenerationSummary.dat
#cleanup at the end
#rm - r ${CWD } / ci - setups

exit 0
