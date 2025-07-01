#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

Sherpa -f charm91.2.dat
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep charm91.2.hepmc3g charm91.2.edm4hep

key4HEPAnalysis -i charm91.2.edm4hep -o charm91.2.root -p 4,-4
