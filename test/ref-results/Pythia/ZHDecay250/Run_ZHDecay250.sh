#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

$PYTHIA8RUNNER/pythiaRunner -f ZHDecay250.dat
$CONVERTHEPMC2EDM4HEP/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep ZHDecay250.hepmc3 ZHDecay250.edm4hep
