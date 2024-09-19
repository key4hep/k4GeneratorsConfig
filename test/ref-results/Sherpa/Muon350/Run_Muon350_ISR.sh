#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

Sherpa -f Muon350_ISR.dat
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Muon350_ISR.hepmc3g Muon350_ISR.edm4hep

$K4GenBuildDir/bin/analyze2f -a 13 -b -13 -i Muon350_ISR.edm4hep -o Muon350_ISR.root
