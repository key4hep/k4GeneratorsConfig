#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

Herwig read Tau350.in
Herwig run Tau350.run
convertHepMC2EDM4HEP -i hepmc2 -o edm4hep Tau350.hepmc Tau350.edm4hep

key4HEPAnalysis -i Tau350.edm4hep -o Tau350.root -p 15,-15
