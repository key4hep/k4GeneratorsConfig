#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

whizard ZH250_ISR.sin
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc ZH250_ISR.edm4hep

key4HEPAnalysis -i ZH250_ISR.edm4hep -o ZH250_ISR.root -p 23,25
