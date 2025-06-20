#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi
if [ -z "${K4GeneratorsConfigBinDir}" ]; then
   K4GeneratorsConfigBinDir = ""
fi

$K4GenBuildDir/bin/pythiaRunner -f Tau350.dat
${K4GeneratorsConfigBinDir}convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Tau350.hepmc3 Tau350.edm4hep

${K4GeneratorsConfigBinDir}key4HEPAnalysis -i Tau350.edm4hep -o Tau350.root -p 15,-15
