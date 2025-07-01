#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

whizard ZHDecay250.sin
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc ZHDecay250.edm4hep

key4HEPAnalysis -i ZHDecay250.edm4hep -o ZHDecay250.root -p 23,25
