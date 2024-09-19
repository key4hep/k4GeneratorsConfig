#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

wget https://whizard.hepforge.org/circe_files/ILC/ilc240.circe
whizard Difermion_Polarized_ISR_BSTilc.sin
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc Difermion_Polarized_ISR_BSTilc.edm4hep

$K4GenBuildDir/bin/analyze2f -a 13 -b -13 -i Difermion_Polarized_ISR_BSTilc.edm4hep -o Difermion_Polarized_ISR_BSTilc.root
