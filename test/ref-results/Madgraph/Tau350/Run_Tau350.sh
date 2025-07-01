#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

mg5_aMC Tau350.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
pythiaLHERunner -f pythiaTau350.cmnd -l unweighted_events.lhe -o Tau350.hepmc
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Tau350.hepmc Tau350.edm4hep

key4HEPAnalysis -i Tau350.edm4hep -o Tau350.root -p 15,-15
