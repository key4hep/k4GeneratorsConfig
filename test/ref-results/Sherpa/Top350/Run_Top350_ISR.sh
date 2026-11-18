#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

Sherpa Top350_ISR.yaml
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Top350_ISR.hepmc Top350_ISR.edm4hep

key4HEPAnalysis -i Top350_ISR.edm4hep -o Top350_ISR.root -p 6,-6
