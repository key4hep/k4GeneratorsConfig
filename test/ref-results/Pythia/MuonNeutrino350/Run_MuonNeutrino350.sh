#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

$K4GenBuildDir/bin/pythiaRunner -f MuonNeutrino350.dat
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep MuonNeutrino350.hepmc3 MuonNeutrino350.edm4hep

$K4GenBuildDir/bin/analyze2f -a 14 -b -14 -i MuonNeutrino350.edm4hep -o MuonNeutrino350.root
