#!/usr/bin/env bash
set -e
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

whizard MuonColliderZH.sin
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc MuonColliderZH.edm4hep

key4HEPAnalysis -i MuonColliderZH.edm4hep -o MuonColliderZH.root -p 23,25
