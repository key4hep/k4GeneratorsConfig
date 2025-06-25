#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

whizard Photon91.0.sin
${K4GENERATORSCONFIG}/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc Photon91.0.edm4hep

${K4GENERATORSCONFIG}/key4HEPAnalysis -i Photon91.0.edm4hep -o Photon91.0.root -p 22,22
