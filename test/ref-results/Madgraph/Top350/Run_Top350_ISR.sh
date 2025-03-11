#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw.hsf.org/key4hep/setup.sh
    if [ -z "${K4GenBuildDir}" ]; then
        export K4GenBuildDir=${K4GENERATORSCONFIG}/../../
        echo "variable K4GenBuildDir was not defined using directory ${K4GenBuildDir} for the executables"
    else
        echo "k4GeneratorsConfig:: using directory ${K4GenBuildDir} for the executables"
    fi
fi

mg5_aMC Top350_ISR.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
$K4GenBuildDir/bin/pythiaLHERunner -f pythiaTop350_ISR.cmnd -l unweighted_events.lhe -o Top350_ISR.hepmc
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Top350_ISR.hepmc Top350_ISR.edm4hep

$K4GenBuildDir/bin/analyze2f -a 6 -b -6 -i Top350_ISR.edm4hep -o Top350_ISR.root
