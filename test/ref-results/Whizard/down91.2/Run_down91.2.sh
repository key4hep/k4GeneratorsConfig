#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

whizard down91.2.sin
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc down91.2.edm4hep

$K4GENERATORSCONFIG/analyze2f -a 1 -b -1 -i down91.2.edm4hep -o down91.2.root
