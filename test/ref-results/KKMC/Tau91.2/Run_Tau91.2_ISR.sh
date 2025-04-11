#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
    if [ -z "${K4GenBuildDir}" ]; then
        export K4GenBuildDir=${K4GENERATORSCONFIG}/../../
        echo "variable K4GenBuildDir was not defined using directory ${K4GenBuildDir} for the executables"
    else
        echo "k4GeneratorsConfig:: using directory ${K4GenBuildDir} for the executables"
    fi
fi

KKMCee -c  Tau91.2_ISR.dat --nevts 10000 -o Tau91.2_ISR.hepmc3
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Tau91.2_ISR.hepmc3 Tau91.2_ISR.edm4hep

$K4GenBuildDir/bin/key4HEPAnalysis -i Tau91.2_ISR.edm4hep -o Tau91.2_ISR.root -p 15,-15
