#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

whizard ZHDecay350.sin
${K4GENERATORSCONFIG}/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc ZHDecay350.edm4hep

${K4GENERATORSCONFIG}/key4HEPAnalysis -i ZHDecay350.edm4hep -o ZHDecay350.root -p 23,25
