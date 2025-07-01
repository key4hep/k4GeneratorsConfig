#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

KKMCee -c  MuonNeutrino91.2_ISR.dat --nevts 10000 -o MuonNeutrino91.2_ISR.hepmc3
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep MuonNeutrino91.2_ISR.hepmc3 MuonNeutrino91.2_ISR.edm4hep

key4HEPAnalysis -i MuonNeutrino91.2_ISR.edm4hep -o MuonNeutrino91.2_ISR.root -p 14,-14
