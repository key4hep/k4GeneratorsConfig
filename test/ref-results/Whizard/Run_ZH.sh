#!/usr/bin/env bash
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
whizard Run_ZH.sin
../../convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc ZH.edm4hep
