#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

mg5_aMC Top350_ISR.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
sed -i '/<header>/,/<\/header>/{//!d}' unweighted_events.lhe
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i lhe -o hepmc3 unweighted_events.lhe Top350_ISR.hepmc
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Top350_ISR.hepmc Top350_ISR.edm4hep

$K4GenBuildDir/bin/analyze2f -a 6 -b -6 -i Top350_ISR.edm4hep -o Top350_ISR.root
