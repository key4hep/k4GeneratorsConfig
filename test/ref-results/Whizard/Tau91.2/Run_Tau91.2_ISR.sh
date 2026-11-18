#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

whizard Tau91.2_ISR.sin
mv proc.hepmc Tau91.2_ISR.hepmc
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Tau91.2_ISR.hepmc Tau91.2_ISR.edm4hep

key4HEPAnalysis -i Tau91.2_ISR.edm4hep -o Tau91.2_ISR.root -p 15,-15
