#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

whizard Tau350.sin
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc Tau350.edm4hep

$K4GENERATORSCONFIG/analyze2f -a 15 -b -15 -i Tau350.edm4hep -f Tau350.root
