#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

babayaga --config Photon91.0.dat
$CONVERTHEPMC2EDM4HEP/convertHepMC2EDM4HEP -i lhe -o hepmc3 events.lhe Photon91.0.hepmc3
$CONVERTHEPMC2EDM4HEP/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Photon91.0.hepmc3 Photon91.0.edm4hep
