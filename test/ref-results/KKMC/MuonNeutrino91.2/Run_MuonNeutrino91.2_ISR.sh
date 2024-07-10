#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

KKMCee -c  MuonNeutrino91.2_ISR.dat -o MuonNeutrino91.2_ISR.hepmc3
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep MuonNeutrino91.2_ISR.hepmc3 MuonNeutrino91.2_ISR.edm4hep
analyze2f -a 14 -b -14 -i MuonNeutrino91.2_ISR.edm4hep -f MuonNeutrino91.2_ISR.root
