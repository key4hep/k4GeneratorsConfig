#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

$PYTHIA8RUNNER/pythiaRunner -f Top1000_ISR.dat
$CONVERTHEPMC2EDM4HEP/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Top1000_ISR.hepmc3 Top1000_ISR.edm4hep
