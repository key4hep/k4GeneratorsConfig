#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

$K4GENERATORSCONFIG/pythiaRunner -f strang91.2.dat
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep strang91.2.hepmc3 strang91.2.edm4hep

$K4GENERATORSCONFIG/analyze2f -a 3 -b -3 -i strang91.2.edm4hep -o strang91.2.root
