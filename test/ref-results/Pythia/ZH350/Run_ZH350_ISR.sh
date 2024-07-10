#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

$K4GENERATORSCONFIG/pythiaRunner -f ZH350_ISR.dat
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep ZH350_ISR.hepmc3 ZH350_ISR.edm4hep
analyze2f -a 23 -b 25 -i ZH350_ISR.edm4hep -f ZH350_ISR.root
