#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

$K4GenBuildDir/bin/pythiaRunner -f Top350_ISR.dat
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Top350_ISR.hepmc3 Top350_ISR.edm4hep

$K4GenBuildDir/bin/analyze2f -a 6 -b -6 -i Top350_ISR.edm4hep -o Top350_ISR.root
