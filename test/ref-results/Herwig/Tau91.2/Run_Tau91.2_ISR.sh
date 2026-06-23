#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

export HERWIGPATH=$(dirname $(which Herwig))/../share/Herwig/
Herwig --repo ${HERWIGPATH}/HerwigDefaults.rpo read Tau91.2_ISR.in
Herwig run Tau91.2_ISR.run
convertHepMC2EDM4HEP -i hepmc2 -o edm4hep Tau91.2_ISR.hepmc2 Tau91.2_ISR.edm4hep

key4HEPAnalysis -i Tau91.2_ISR.edm4hep -o Tau91.2_ISR.root -p 15,-15
