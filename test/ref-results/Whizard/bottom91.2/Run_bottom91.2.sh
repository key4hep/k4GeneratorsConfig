#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
    if [ -z "${K4GenBuildDir}" ]; then
        export K4GenBuildDir=${K4GENERATORSCONFIG}/../../
        echo "variable K4GenBuildDir was not defined using directory ${K4GenBuildDir} for the executables"
    else
        echo "k4GeneratorsConfig:: using directory ${K4GenBuildDir} for the executables"
    fi
fi

whizard bottom91.2.sin
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc bottom91.2.edm4hep

$K4GENERATORSCONFIG/key4HEPAnalysis -i bottom91.2.edm4hep -o bottom91.2.root -p 2,-2
