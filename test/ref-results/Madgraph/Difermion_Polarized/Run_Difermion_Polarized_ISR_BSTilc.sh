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

mg5_aMC Difermion_Polarized_ISR_BSTilc.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
$K4GenBuildDir/bin/pythiaLHERunner -f pythiaDifermion_Polarized_ISR_BSTilc.cmnd -l unweighted_events.lhe -o Difermion_Polarized_ISR_BSTilc.hepmc
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Difermion_Polarized_ISR_BSTilc.hepmc Difermion_Polarized_ISR_BSTilc.edm4hep

$K4GenBuildDir/bin/analyze2f -a 13 -b -13 -i Difermion_Polarized_ISR_BSTilc.edm4hep -o Difermion_Polarized_ISR_BSTilc.root
