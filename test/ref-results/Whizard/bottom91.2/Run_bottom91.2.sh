#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

whizard bottom91.2.sin
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc bottom91.2.edm4hep

key4HEPAnalysis -i bottom91.2.edm4hep -o bottom91.2.root -p 2,-2
