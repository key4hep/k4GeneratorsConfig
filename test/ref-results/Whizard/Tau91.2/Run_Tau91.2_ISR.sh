#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

whizard Tau91.2_ISR.sin
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc Tau91.2_ISR.edm4hep

$K4GenBuildDir/bin/analyze2f -a 15 -b -15 -i Tau91.2_ISR.edm4hep -o Tau91.2_ISR.root
