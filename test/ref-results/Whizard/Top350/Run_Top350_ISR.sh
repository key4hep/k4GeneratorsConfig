#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

whizard Top350_ISR.sin
${K4GENERATORSCONFIG}/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc Top350_ISR.edm4hep

${K4GENERATORSCONFIG}/key4HEPAnalysis -i Top350_ISR.edm4hep -o Top350_ISR.root -p 6,-6
