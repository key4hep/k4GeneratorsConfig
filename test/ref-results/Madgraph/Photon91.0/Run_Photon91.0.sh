#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

mg5_aMC Photon91.0.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
sed -i '/<header>/,/<\/header>/{//!d}' unweighted_events.lhe
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i lhe -o hepmc3 unweighted_events.lhe Photon91.0.hepmc
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Photon91.0.hepmc Photon91.0.edm4hep
