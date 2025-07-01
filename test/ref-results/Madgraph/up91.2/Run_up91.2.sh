#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

mg5_aMC up91.2.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
sed -i '/<header>/,/<\/header>/{//!d}' unweighted_events.lhe
convertHepMC2EDM4HEP -i lhe -o hepmc3 unweighted_events.lhe up91.2.hepmc
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep up91.2.hepmc up91.2.edm4hep

key4HEPAnalysis -i up91.2.edm4hep -o up91.2.root -p 2,-2 
