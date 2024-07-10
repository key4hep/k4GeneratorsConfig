#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

cat Photon91.0.dat | babayaga-fcc.exe
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i lhe -o hepmc3 events.lhe Photon91.0.hepmc3
$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Photon91.0.hepmc3 Photon91.0.edm4hep
