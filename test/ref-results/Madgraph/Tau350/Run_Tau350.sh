#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

mg5_aMC Tau350.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
$K4GenBuildDir/bin/pythiaLHERunner -f pythiaTau350.cmnd -l unweighted_events.lhe -o Tau350.hepmc
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Tau350.hepmc Tau350.edm4hep

$K4GenBuildDir/bin/analyze2f -a 15 -b -15 -i Tau350.edm4hep -o Tau350.root
