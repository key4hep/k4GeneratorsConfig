#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

export HERWIGPATH=$(dirname $(which Herwig))/../share/Herwig/
Herwig --append-read ${HERWIGPATH}/defaults init
Herwig --append-read ${HERWIGPATH} read ZH350_ISR.in
Herwig run ZH350_ISR.run
convertHepMC2EDM4HEP -i hepmc2 -o edm4hep ZH350_ISR.hepmc2 ZH350_ISR.edm4hep

key4HEPAnalysis -i ZH350_ISR.edm4hep -o ZH350_ISR.root -p 23,25
