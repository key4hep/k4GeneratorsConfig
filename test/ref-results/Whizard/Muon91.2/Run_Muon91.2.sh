#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

whizard Muon91.2.sin
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc Muon91.2.edm4hep

$K4GenBuildDir/bin/analyze2f -a 13 -b -13 -i Muon91.2.edm4hep -o Muon91.2.root
