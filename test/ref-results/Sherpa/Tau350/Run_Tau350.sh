#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

Sherpa -f Tau350.dat
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Tau350.hepmc3g Tau350.edm4hep

$K4GENERATORSCONFIG/analyze2f -a 15 -b -15 -i Tau350.edm4hep -f Tau350.root
