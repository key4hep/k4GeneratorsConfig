#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

$K4GENERATORSCONFIG/pythiaRunner -f ZHDecay250.dat
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep ZHDecay250.hepmc3 ZHDecay250.edm4hep
analyze2f -a 23 -b 25 -i ZHDecay250.edm4hep -f ZHDecay250.root
