#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

$K4GENERATORSCONFIG/pythiaRunner -f bottom91.2.dat
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep bottom91.2.hepmc3 bottom91.2.edm4hep

$K4GENERATORSCONFIG/analyze2f -a 2 -b -2 -i bottom91.2.edm4hep -o bottom91.2.root
