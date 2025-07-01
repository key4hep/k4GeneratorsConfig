#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

mg5_aMC MuonNeutrino350.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
pythiaLHERunner -f pythiaMuonNeutrino350.cmnd -l unweighted_events.lhe -o MuonNeutrino350.hepmc
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep MuonNeutrino350.hepmc MuonNeutrino350.edm4hep

key4HEPAnalysis -i MuonNeutrino350.edm4hep -o MuonNeutrino350.root -p 14,-14
