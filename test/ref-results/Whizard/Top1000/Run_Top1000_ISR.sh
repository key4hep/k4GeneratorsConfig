#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

whizard Top1000_ISR.sin
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc Top1000_ISR.edm4hep

$K4GenBuildDir/bin/analyze2f -a 6 -b -6 -i Top1000_ISR.edm4hep -o Top1000_ISR.root
