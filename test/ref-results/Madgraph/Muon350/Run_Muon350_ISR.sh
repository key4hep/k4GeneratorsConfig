#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

mg5_aMC Muon350_ISR.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
pythiaLHERunner -f pythiaMuon350_ISR.cmnd -l unweighted_events.lhe -o Muon350_ISR.hepmc
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Muon350_ISR.hepmc Muon350_ISR.edm4hep

key4HEPAnalysis -i Muon350_ISR.edm4hep -o Muon350_ISR.root -p 13,-13
