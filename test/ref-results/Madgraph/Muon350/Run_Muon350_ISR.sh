#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

mg5_aMC Muon350_ISR.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
sed -i '/<header>/,/<\/header>/{//!d}' unweighted_events.lhe
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i lhe -o hepmc3 unweighted_events.lhe Muon350_ISR.hepmc
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Muon350_ISR.hepmc Muon350_ISR.edm4hep
analyze2f -a 13 -b -13 -i Muon350_ISR.edm4hep -f Muon350_ISR.root
