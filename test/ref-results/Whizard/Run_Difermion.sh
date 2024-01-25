#!/usr/bin/env bash
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
whizard Run_Difermion.sin
../../convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc Difermion.edm4hep
