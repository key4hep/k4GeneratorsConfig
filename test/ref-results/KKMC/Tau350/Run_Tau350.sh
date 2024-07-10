#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

KKMCee -c  Tau350.dat -o Tau350.hepmc3
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Tau350.hepmc3 Tau350.edm4hep
analyze2f -a 15 -b -15 -i Tau350.edm4hep -f Tau350.root
