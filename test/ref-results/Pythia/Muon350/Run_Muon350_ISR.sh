#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi
if [ -z "${K4GeneratorsConfigBinDir}" ]; then
   K4GeneratorsConfigBinDir=""
fi

${K4GeneratorsConfigBinDir}pythiaRunner -f Muon350_ISR.dat
${K4GeneratorsConfigBinDir}convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Muon350_ISR.hepmc3 Muon350_ISR.edm4hep

${K4GeneratorsConfigBinDir}key4HEPAnalysis -i Muon350_ISR.edm4hep -o Muon350_ISR.root -p 13,-13
