#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

Sherpa -f Difermion_Polarized_ISR_BSTilc.dat
./makelibs 
Sherpa -f Difermion_Polarized_ISR_BSTilc.dat
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Difermion_Polarized_ISR_BSTilc.hepmc3 Difermion_Polarized_ISR_BSTilc.edm4hep

key4HEPAnalysis -i Difermion_Polarized_ISR_BSTilc.edm4hep -o Difermion_Polarized_ISR_BSTilc.root -p 13,-13
