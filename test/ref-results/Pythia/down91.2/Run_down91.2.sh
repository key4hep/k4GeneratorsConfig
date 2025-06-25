#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

$K4GENERATORSCONFIG/pythiaRunner -f down91.2.dat
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep down91.2.hepmc3 down91.2.edm4hep

$K4GENERATORSCONFIG/key4HEPAnalysis -i down91.2.edm4hep -o down91.2.root -p 1,-1
