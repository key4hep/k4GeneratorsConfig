#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

mg5_aMC ZH250_ISR.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
pythiaLHERunner -f pythiaZH250_ISR.cmnd -l unweighted_events.lhe -o ZH250_ISR.hepmc
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep ZH250_ISR.hepmc ZH250_ISR.edm4hep

key4HEPAnalysis -i ZH250_ISR.edm4hep -o ZH250_ISR.root -p 23,25
