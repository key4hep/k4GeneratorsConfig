#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi
if [ -z "${K4GeneratorsConfigBinDir}" ]; then
   K4GeneratorsConfigBinDir=""
fi

mg5_aMC Tau350.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
${K4GeneratorsConfigBinDir}pythiaLHERunner -f pythiaTau350.cmnd -l unweighted_events.lhe -o Tau350.hepmc
${K4GeneratorsConfigBinDir}convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Tau350.hepmc Tau350.edm4hep

${K4GeneratorsConfigBinDir}key4HEPAnalysis -i Tau350.edm4hep -o Tau350.root -p 15,-15
