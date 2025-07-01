#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

Sherpa -f MuonNeutrino350.dat
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep MuonNeutrino350.hepmc3 MuonNeutrino350.edm4hep

key4HEPAnalysis -i MuonNeutrino350.edm4hep -o MuonNeutrino350.root -p 14,-14
