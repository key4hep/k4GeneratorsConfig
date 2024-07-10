#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

$K4GENERATORSCONFIG/pythiaRunner -f Top1000_ISR.dat
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Top1000_ISR.hepmc3 Top1000_ISR.edm4hep

$K4GENERATORSCONFIG/analyze2f -a 6 -b -6 -i Top1000_ISR.edm4hep -f Top1000_ISR.root
