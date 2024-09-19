#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

whizard charm91.2.sin
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc charm91.2.edm4hep

$K4GENERATORSCONFIG/analyze2f -a 4 -b -4 -i charm91.2.edm4hep -o charm91.2.root
