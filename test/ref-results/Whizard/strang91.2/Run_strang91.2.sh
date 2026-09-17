#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

whizard strang91.2.sin
whizard proc.hepmc strang91.2.hepmc
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep strang91.2.hepmc strang91.2.edm4hep

key4HEPAnalysis -i strang91.2.edm4hep -o strang91.2.root -p 3,-3
