#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

$K4GENERATORSCONFIG/pythiaRunner -f ZHDecay350.dat
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep ZHDecay350.hepmc3 ZHDecay350.edm4hep

$K4GENERATORSCONFIG/analyze2f -a 23 -b 25 -i ZHDecay350.edm4hep -o ZHDecay350.root
