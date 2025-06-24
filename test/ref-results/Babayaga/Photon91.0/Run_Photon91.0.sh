#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi
if [ -z "${K4GeneratorsConfigBinDir}" ]; then
   K4GeneratorsConfigBinDir=""
fi

cat Photon91.0.dat | babayaga-fcc.exe
${K4GeneratorsConfigBinDir}convertHepMC2EDM4HEP -i lhe -o hepmc3 events.lhe Photon91.0.hepmc3
${K4GeneratorsConfigBinDir}convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Photon91.0.hepmc3 Photon91.0.edm4hep

${K4GeneratorsConfigBinDir}key4HEPAnalysis -i Photon91.0.edm4hep -o Photon91.0.root -p 22,22
