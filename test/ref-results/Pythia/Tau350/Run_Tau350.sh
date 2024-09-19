#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

$K4GenBuildDir/bin/pythiaRunner -f Tau350.dat
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Tau350.hepmc3 Tau350.edm4hep

$K4GenBuildDir/bin/analyze2f -a 15 -b -15 -i Tau350.edm4hep -o Tau350.root
