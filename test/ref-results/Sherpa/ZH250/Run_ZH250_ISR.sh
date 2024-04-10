#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

Sherpa -f Run_ZH250_ISR.dat
$CONVERTHEPMC2EDM4HEP/convertHepMC2EDM4HEP -i hepmc2 -o edm4hep ZH250_ISR.hepmc2g ZH250_ISR.edm4hep
