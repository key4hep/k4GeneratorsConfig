#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

export HERWIGPATH=$(dirname $(which Herwig))/../share/Herwig/
Herwig --append-read ${HERWIGPATH}/defaults init
Herwig --append-read ${HERWIGPATH} read MuonNeutrino91.2_ISR.in
Herwig run MuonNeutrino91.2_ISR.run
convertHepMC2EDM4HEP -i hepmc2 -o edm4hep MuonNeutrino91.2_ISR.hepmc2 MuonNeutrino91.2_ISR.edm4hep

key4HEPAnalysis -i MuonNeutrino91.2_ISR.edm4hep -o MuonNeutrino91.2_ISR.root -p 14,-14
