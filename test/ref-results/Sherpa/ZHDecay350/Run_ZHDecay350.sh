#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

Sherpa -f Run_ZHDecay350.dat
./makelibs 
Sherpa -f Run_ZHDecay350.dat
$CONVERTHEPMC2EDM4HEP/convertHepMC2EDM4HEP -i hepmc2 -o edm4hep ZHDecay350.hepmc2g ZHDecay350.edm4hep
