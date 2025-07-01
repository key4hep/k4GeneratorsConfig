#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

Sherpa -f ZHDecay350.dat
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep ZHDecay350.hepmc3 ZHDecay350.edm4hep

key4HEPAnalysis -i ZHDecay350.edm4hep -o ZHDecay350.root -p 23,25
