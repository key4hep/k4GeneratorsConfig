#!/usr/bin/env bash
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
Sherpa -f Run_TauNeutrino.dat
$CONVERTHEPMC2EDM4HEP/convertHepMC2EDM4HEP -i hepmc2 -o edm4hep TauNeutrino.hepmc2g TauNeutrino.edm4hep
