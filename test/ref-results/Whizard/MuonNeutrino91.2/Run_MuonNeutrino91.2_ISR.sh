#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

whizard MuonNeutrino91.2_ISR.sin
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc MuonNeutrino91.2_ISR.edm4hep

key4HEPAnalysis -i MuonNeutrino91.2_ISR.edm4hep -o MuonNeutrino91.2_ISR.root -p 14,-14
