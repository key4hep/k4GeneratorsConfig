#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

whizard MuonNeutrino350.sin
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc MuonNeutrino350.edm4hep

$K4GENERATORSCONFIG/analyze2f -a 14 -b -14 -i MuonNeutrino350.edm4hep -o MuonNeutrino350.root
