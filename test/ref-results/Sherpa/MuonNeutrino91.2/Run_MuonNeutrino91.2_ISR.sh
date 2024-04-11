#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

Sherpa -f MuonNeutrino91.2_ISR.dat
$CONVERTHEPMC2EDM4HEP/convertHepMC2EDM4HEP -i hepmc2 -o edm4hep MuonNeutrino91.2_ISR.hepmc2g MuonNeutrino91.2_ISR.edm4hep
