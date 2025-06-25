#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

mg5_aMC Top350_ISR.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
${K4GENERATORSCONFIG}/pythiaLHERunner -f pythiaTop350_ISR.cmnd -l unweighted_events.lhe -o Top350_ISR.hepmc
${K4GENERATORSCONFIG}/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Top350_ISR.hepmc Top350_ISR.edm4hep

${K4GENERATORSCONFIG}/key4HEPAnalysis -i Top350_ISR.edm4hep -o Top350_ISR.root -p 6,-6
