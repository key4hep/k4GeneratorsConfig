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

whizard Muon350_ISR.sin
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc Muon350_ISR.edm4hep

$K4GenBuildDir/bin/analyze2f -a 13 -b -13 -i Muon350_ISR.edm4hep -o Muon350_ISR.root
