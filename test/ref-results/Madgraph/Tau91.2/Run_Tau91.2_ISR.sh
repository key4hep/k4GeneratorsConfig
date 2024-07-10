#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

mg5_aMC Tau91.2_ISR.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
sed -i '/<header>/,/<\/header>/{//!d}' unweighted_events.lhe
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i lhe -o hepmc3 unweighted_events.lhe Tau91.2_ISR.hepmc
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Tau91.2_ISR.hepmc Tau91.2_ISR.edm4hep
analyze2f -a 15 -b -15 -i Tau91.2_ISR.edm4hep -f Tau91.2_ISR.root
