#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

Herwig read ZH250_ISR.in
Herwig run ZH250_ISR.run
convertHepMC2EDM4HEP -i hepmc2 -o edm4hep ZH250_ISR.hepmc2 ZH250_ISR.edm4hep

key4HEPAnalysis -i ZH250_ISR.edm4hep -o ZH250_ISR.root -p 23,25
