#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi
if [ -z "${K4GeneratorsConfigBinDir}" ]; then
   K4GeneratorsConfigBinDir=""
fi

Sherpa -f ZH350_ISR.dat
${K4GeneratorsConfigBinDir}convertHepMC2EDM4HEP -i hepmc3 -o edm4hep ZH350_ISR.hepmc3 ZH350_ISR.edm4hep

${K4GeneratorsConfigBinDir}key4HEPAnalysis -i ZH350_ISR.edm4hep -o ZH350_ISR.root -p 23,25
