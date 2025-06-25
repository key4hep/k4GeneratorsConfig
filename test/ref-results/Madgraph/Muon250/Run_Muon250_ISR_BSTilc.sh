#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

mg5_aMC Muon250_ISR_BSTilc.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
${K4GENERATORSCONFIG}/pythiaLHERunner -f pythiaMuon250_ISR_BSTilc.cmnd -l unweighted_events.lhe -o Muon250_ISR_BSTilc.hepmc
${K4GENERATORSCONFIG}/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Muon250_ISR_BSTilc.hepmc Muon250_ISR_BSTilc.edm4hep

${K4GENERATORSCONFIG}/key4HEPAnalysis -i Muon250_ISR_BSTilc.edm4hep -o Muon250_ISR_BSTilc.root -p 13,-13
