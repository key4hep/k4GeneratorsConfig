#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

Sherpa -f Difermion_Polarized.dat
./makelibs 
Sherpa -f Difermion_Polarized.dat
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Difermion_Polarized.hepmc3 Difermion_Polarized.edm4hep

key4HEPAnalysis -i Difermion_Polarized.edm4hep -o Difermion_Polarized.root -p 13,-13
