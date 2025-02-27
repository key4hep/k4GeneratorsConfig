#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

Sherpa -f Photon91.0.dat
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Photon91.0.hepmc3 Photon91.0.edm4hep

$K4GenBuildDir/bin/analyze2f -a 22 -b 22 -i Photon91.0.edm4hep -o Photon91.0.root
