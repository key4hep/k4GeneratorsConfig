#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
fi

mg5_aMC Top1000_ISR.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
$K4GenBuildDir/bin/pythiaLHERunner -f pythiaTop1000_ISR.cmnd -l unweighted_events.lhe -o Top1000_ISR.hepmc
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Top1000_ISR.hepmc Top1000_ISR.edm4hep

$K4GenBuildDir/bin/analyze2f -a 6 -b -6 -i Top1000_ISR.edm4hep -o Top1000_ISR.root
