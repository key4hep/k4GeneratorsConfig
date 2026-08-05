#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

Herwig read Muon91.2.in
Herwig run Muon91.2.run
convertHepMC2EDM4HEP -i hepmc2 -o edm4hep Muon91.2.hepmc Muon91.2.edm4hep

key4HEPAnalysis -i Muon91.2.edm4hep -o Muon91.2.root -p 13,-13
