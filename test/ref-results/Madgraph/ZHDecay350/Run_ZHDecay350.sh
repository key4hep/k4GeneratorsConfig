#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

mg5_aMC ZHDecay350.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
pythiaLHERunner -f pythiaZHDecay350.cmnd -l unweighted_events.lhe -o ZHDecay350.hepmc
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep ZHDecay350.hepmc ZHDecay350.edm4hep

key4HEPAnalysis -i ZHDecay350.edm4hep -o ZHDecay350.root -p 23,25
