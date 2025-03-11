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

mg5_aMC Photon91.0.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
$K4GenBuildDir/bin/pythiaLHERunner -f pythiaPhoton91.0.cmnd -l unweighted_events.lhe -o Photon91.0.hepmc
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Photon91.0.hepmc Photon91.0.edm4hep

$K4GenBuildDir/bin/analyze2f -a 22 -b 22 -i Photon91.0.edm4hep -o Photon91.0.root
