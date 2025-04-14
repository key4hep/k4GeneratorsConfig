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

$K4GenBuildDir/bin/pythiaRunner -f MuonNeutrino91.2_ISR.dat
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep MuonNeutrino91.2_ISR.hepmc3 MuonNeutrino91.2_ISR.edm4hep

$K4GenBuildDir/bin/key4HEPAnalysis -i MuonNeutrino91.2_ISR.edm4hep -o MuonNeutrino91.2_ISR.root -p 14,-14
