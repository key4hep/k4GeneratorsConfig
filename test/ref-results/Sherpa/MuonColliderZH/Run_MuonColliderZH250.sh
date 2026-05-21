#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

Sherpa -f MuonColliderZH250.dat
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep MuonColliderZH250.hepmc3 MuonColliderZH250.edm4hep

key4HEPAnalysis -i MuonColliderZH250.edm4hep -o MuonColliderZH250.root -p 23,25
