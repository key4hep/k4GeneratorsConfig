#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

whizard ZH250_ISR.sin
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc ZH250_ISR.edm4hep

$K4GenBuildDir/bin/analyze2f -a 23 -b 25 -i ZH250_ISR.edm4hep -o ZH250_ISR.root
