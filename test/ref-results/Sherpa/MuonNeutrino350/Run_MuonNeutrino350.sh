#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi
if [ -z "${K4GeneratorsConfigBinDir}" ]; then
   K4GeneratorsConfigBinDir=""
fi

Sherpa -f MuonNeutrino350.dat
${K4GeneratorsConfigBinDir}convertHepMC2EDM4HEP -i hepmc3 -o edm4hep MuonNeutrino350.hepmc3 MuonNeutrino350.edm4hep

${K4GeneratorsConfigBinDir}key4HEPAnalysis -i MuonNeutrino350.edm4hep -o MuonNeutrino350.root -p 14,-14
