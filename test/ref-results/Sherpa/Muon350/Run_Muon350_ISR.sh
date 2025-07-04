#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

Sherpa -f Muon350_ISR.dat
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Muon350_ISR.hepmc3 Muon350_ISR.edm4hep

key4HEPAnalysis -i Muon350_ISR.edm4hep -o Muon350_ISR.root -p 13,-13
