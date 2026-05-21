#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

mg5_aMC MuonColliderZH.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
pythiaLHERunner -f pythiaMuonColliderZH.cmnd -l unweighted_events.lhe -o MuonColliderZH.hepmc
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep MuonColliderZH.hepmc MuonColliderZH.edm4hep

key4HEPAnalysis -i MuonColliderZH.edm4hep -o MuonColliderZH.root -p 23,25
