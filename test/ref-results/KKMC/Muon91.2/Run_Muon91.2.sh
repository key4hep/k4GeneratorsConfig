#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi
if [ -z "${K4GeneratorsConfigBinDir}" ]; then
   K4GeneratorsConfigBinDir=""
fi

KKMCee -c  Muon91.2.dat --nevts 10000 -o Muon91.2.hepmc3
${K4GeneratorsConfigBinDir}convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Muon91.2.hepmc3 Muon91.2.edm4hep

${K4GeneratorsConfigBinDir}key4HEPAnalysis -i Muon91.2.edm4hep -o Muon91.2.root -p 13,-13
