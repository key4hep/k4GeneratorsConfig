#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

pythiaRunner -f ZH350_ISR.dat
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep ZH350_ISR.hepmc3 ZH350_ISR.edm4hep

key4HEPAnalysis -i ZH350_ISR.edm4hep -o ZH350_ISR.root -p 23,25
