#!/usr/bin/env bash
set -e
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

mg5_aMC Difermion_Polarized.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
pythiaLHERunner -f pythiaDifermion_Polarized.cmnd -l unweighted_events.lhe -o Difermion_Polarized.hepmc
convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Difermion_Polarized.hepmc Difermion_Polarized.edm4hep

key4HEPAnalysis -i Difermion_Polarized.edm4hep -o Difermion_Polarized.root -p 13,-13
