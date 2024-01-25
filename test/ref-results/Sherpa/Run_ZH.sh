#!/usr/bin/env bash
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
Sherpa -f Run_ZH.dat
../../convertHepMC2EDM4HEP -i hepmc2 -o edm4hep ZH.hepmc2g ZH.edm4hep
