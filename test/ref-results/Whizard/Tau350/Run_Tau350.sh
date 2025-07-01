#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

whizard Tau350.sin
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc Tau350.edm4hep

key4HEPAnalysis -i Tau350.edm4hep -o Tau350.root -p 15,-15
