#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

whizard Top1000_ISR.sin
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc Top1000_ISR.edm4hep

key4HEPAnalysis -i Top1000_ISR.edm4hep -o Top1000_ISR.root -p 6,-6
