#!/usr/bin/env bash
set -e
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

whizard Difermion_Polarized.sin
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc Difermion_Polarized.edm4hep

key4HEPAnalysis -i Difermion_Polarized.edm4hep -o Difermion_Polarized.root -p 13,-13
