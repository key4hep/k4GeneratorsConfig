#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

whizard Photon91.0.sin
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc Photon91.0.edm4hep

$K4GenBuildDir/bin/analyze2f -a 22 -b 22 -i Photon91.0.edm4hep -o Photon91.0.root
