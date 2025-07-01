#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

Sherpa -f Top1000_ISR.dat
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Top1000_ISR.hepmc3 Top1000_ISR.edm4hep

key4HEPAnalysis -i Top1000_ISR.edm4hep -o Top1000_ISR.root -p 6,-6
