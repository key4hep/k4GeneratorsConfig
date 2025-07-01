#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

cat Photon91.0.dat | babayaga-fcc.exe
convertHepMC2EDM4HEP -i lhe -o edm4hep events.lhe Photon91.0.edm4hep

key4HEPAnalysis -i Photon91.0.edm4hep -o Photon91.0.root -p 22,22
