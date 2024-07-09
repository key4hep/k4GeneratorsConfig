#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

$PYTHIA8RUNNER/pythiaRunner -f ZHDecay350.dat
$CONVERTHEPMC2EDM4HEP/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep ZHDecay350.hepmc3 ZHDecay350.edm4hep
