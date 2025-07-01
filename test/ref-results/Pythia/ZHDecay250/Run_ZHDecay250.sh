#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

pythiaRunner -f ZHDecay250.dat
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep ZHDecay250.hepmc3 ZHDecay250.edm4hep

key4HEPAnalysis -i ZHDecay250.edm4hep -o ZHDecay250.root -p 23,25
