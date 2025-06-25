#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

KKMCee -c  bottom91.2.dat -o bottom91.2.hepmc3
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep bottom91.2.hepmc3 bottom91.2.edm4hep

$K4GENERATORSCONFIG/key4HEPAnalysis -i bottom91.2.edm4hep -o bottom91.2.root -p 2,-2
