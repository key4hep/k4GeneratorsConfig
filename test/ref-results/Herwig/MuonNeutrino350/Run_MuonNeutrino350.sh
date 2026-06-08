#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

export HERWIGPATH=$(dirname $(which Herwig))/../share/Herwig/
Herwig --append-read ${HERWIGPATH}/defaults init
Herwig --append-read ${HERWIGPATH} read MuonNeutrino350.in
Herwig run MuonNeutrino350.run
convertHepMC2EDM4HEP -i hepmc2 -o edm4hep MuonNeutrino350.hepmc2 MuonNeutrino350.edm4hep

key4HEPAnalysis -i MuonNeutrino350.edm4hep -o MuonNeutrino350.root -p 14,-14
