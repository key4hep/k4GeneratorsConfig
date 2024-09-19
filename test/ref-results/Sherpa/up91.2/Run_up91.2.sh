#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

Sherpa -f up91.2.dat
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep up91.2.hepmc3g up91.2.edm4hep

$K4GENERATORSCONFIG/analyze2f -a 2 -b -2 -i up91.2.edm4hep -o up91.2.root
