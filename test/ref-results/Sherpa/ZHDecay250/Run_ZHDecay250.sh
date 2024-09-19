#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

Sherpa -f ZHDecay250.dat
./makelibs 
Sherpa -f ZHDecay250.dat
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep ZHDecay250.hepmc3g ZHDecay250.edm4hep

$K4GenBuildDir/bin/analyze2f -a 23 -b 25 -i ZHDecay250.edm4hep -o ZHDecay250.root
