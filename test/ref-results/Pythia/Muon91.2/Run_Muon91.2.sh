#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

$K4GENERATORSCONFIG/pythiaRunner -f Muon91.2.dat
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Muon91.2.hepmc3 Muon91.2.edm4hep

$K4GENERATORSCONFIG/analyze2f -a 13 -b -13 -i Muon91.2.edm4hep -o Muon91.2.root
