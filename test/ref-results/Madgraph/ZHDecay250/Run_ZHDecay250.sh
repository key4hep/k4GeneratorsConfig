#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

mg5_aMC ZHDecay250.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
$K4GenBuildDir/bin/pythiaLHERunner -f pythiaZHDecay250.cmnd -l unweighted_events.lhe -o ZHDecay250.hepmc
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep ZHDecay250.hepmc ZHDecay250.edm4hep

$K4GenBuildDir/bin/analyze2f -a 23 -b 25 -i ZHDecay250.edm4hep -o ZHDecay250.root
