#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

export HERWIGPATH=$(dirname $(which Herwig))/../share/Herwig/
Herwig --append-read ${HERWIGPATH}/defaults init
Herwig --append-read ${HERWIGPATH} read Muon350_ISR.in
Herwig run Muon350_ISR.run
convertHepMC2EDM4HEP -i hepmc2 -o edm4hep Muon350_ISR.hepmc2 Muon350_ISR.edm4hep

key4HEPAnalysis -i Muon350_ISR.edm4hep -o Muon350_ISR.root -p 13,-13
