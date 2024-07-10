#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

wget https://whizard.hepforge.org/circe_files/CEPC/cepc240.circe
whizard Muon240_ISR_BSTcepc.sin
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc Muon240_ISR_BSTcepc.edm4hep

$K4GENERATORSCONFIG/analyze2f -a 13 -b -13 -i Muon240_ISR_BSTcepc.edm4hep -f Muon240_ISR_BSTcepc.root
