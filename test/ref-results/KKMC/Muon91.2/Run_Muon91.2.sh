#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

KKMCee -c  Muon91.2.dat --nevts 100 -o Muon91.2.hepmc3
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Muon91.2.hepmc3 Muon91.2.edm4hep

$K4GenBuildDir/bin/analyze2f -a 13 -b -13 -i Muon91.2.edm4hep -o Muon91.2.root
