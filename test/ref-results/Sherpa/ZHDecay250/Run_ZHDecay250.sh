#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

Sherpa -f ZHDecay250.dat
${K4GENERATORSCONFIG}/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep ZHDecay250.hepmc3 ZHDecay250.edm4hep

${K4GENERATORSCONFIG}/key4HEPAnalysis -i ZHDecay250.edm4hep -o ZHDecay250.root -p 23,25
