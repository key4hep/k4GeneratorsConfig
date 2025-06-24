#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi
if [ -z "${K4GeneratorsConfigBinDir}" ]; then
   K4GeneratorsConfigBinDir=""
fi

mg5_aMC Photon91.0.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
${K4GeneratorsConfigBinDir}pythiaLHERunner -f pythiaPhoton91.0.cmnd -l unweighted_events.lhe -o Photon91.0.hepmc
${K4GeneratorsConfigBinDir}convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Photon91.0.hepmc Photon91.0.edm4hep

${K4GeneratorsConfigBinDir}key4HEPAnalysis -i Photon91.0.edm4hep -o Photon91.0.root -p 22,22
