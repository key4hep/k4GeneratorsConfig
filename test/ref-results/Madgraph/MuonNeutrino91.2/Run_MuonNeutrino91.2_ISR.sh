#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

mg5_aMC MuonNeutrino91.2_ISR.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
${K4GENERATORSCONFIG}/pythiaLHERunner -f pythiaMuonNeutrino91.2_ISR.cmnd -l unweighted_events.lhe -o MuonNeutrino91.2_ISR.hepmc
${K4GENERATORSCONFIG}/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep MuonNeutrino91.2_ISR.hepmc MuonNeutrino91.2_ISR.edm4hep

${K4GENERATORSCONFIG}/key4HEPAnalysis -i MuonNeutrino91.2_ISR.edm4hep -o MuonNeutrino91.2_ISR.root -p 14,-14
