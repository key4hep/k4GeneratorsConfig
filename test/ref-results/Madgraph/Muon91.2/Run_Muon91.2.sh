#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

mg5_aMC Muon91.2.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
pythiaLHERunner -f pythiaMuon91.2.cmnd -l unweighted_events.lhe -o Muon91.2.hepmc
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Muon91.2.hepmc Muon91.2.edm4hep

key4HEPAnalysis -i Muon91.2.edm4hep -o Muon91.2.root -p 13,-13
