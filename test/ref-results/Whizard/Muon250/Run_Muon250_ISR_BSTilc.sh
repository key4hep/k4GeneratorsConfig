#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

wget https://whizard.hepforge.org/circe_files/ILC/250_SetA_ee024.circe
whizard Muon250_ISR_BSTilc.sin
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc Muon250_ISR_BSTilc.edm4hep

key4HEPAnalysis -i Muon250_ISR_BSTilc.edm4hep -o Muon250_ISR_BSTilc.root -p 13,-13
