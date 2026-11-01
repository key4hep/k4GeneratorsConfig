#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

Sherpa Difermion_Polarized.yaml
./makelibs 
Sherpa Difermion_Polarized.yaml
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Difermion_Polarized.hepmc Difermion_Polarized.edm4hep

key4HEPAnalysis -i Difermion_Polarized.edm4hep -o Difermion_Polarized.root -p 13,-13
