#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

KKMCee -c  strang91.2.dat -o strang91.2.hepmc3
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep strang91.2.hepmc3 strang91.2.edm4hep

key4HEPAnalysis -i strang91.2.edm4hep -o strang91.2.root -p 3,-3
