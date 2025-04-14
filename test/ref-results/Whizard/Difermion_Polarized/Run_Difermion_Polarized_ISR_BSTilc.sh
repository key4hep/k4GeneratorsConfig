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

wget https://whizard.hepforge.org/circe_files/ILC/250_SetA_ee024.circe
whizard Difermion_Polarized_ISR_BSTilc.sin
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc Difermion_Polarized_ISR_BSTilc.edm4hep

$K4GenBuildDir/bin/key4HEPAnalysis -i Difermion_Polarized_ISR_BSTilc.edm4hep -o Difermion_Polarized_ISR_BSTilc.root -p 13,-13
