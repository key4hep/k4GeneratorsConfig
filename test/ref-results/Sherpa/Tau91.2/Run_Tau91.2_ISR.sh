#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

Sherpa -f Tau91.2_ISR.dat
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Tau91.2_ISR.hepmc3g Tau91.2_ISR.edm4hep

$K4GENERATORSCONFIG/analyze2f -a 15 -b -15 -i Tau91.2_ISR.edm4hep -f Tau91.2_ISR.root
