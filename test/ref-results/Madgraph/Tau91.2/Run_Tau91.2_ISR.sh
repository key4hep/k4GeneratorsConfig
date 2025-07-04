#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

mg5_aMC Tau91.2_ISR.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
pythiaLHERunner -f pythiaTau91.2_ISR.cmnd -l unweighted_events.lhe -o Tau91.2_ISR.hepmc
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Tau91.2_ISR.hepmc Tau91.2_ISR.edm4hep

key4HEPAnalysis -i Tau91.2_ISR.edm4hep -o Tau91.2_ISR.root -p 15,-15
