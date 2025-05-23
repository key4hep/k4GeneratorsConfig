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

cat Photon91.0.dat | babayaga-fcc.exe
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i lhe -o hepmc3 events.lhe Photon91.0.hepmc3
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep Photon91.0.hepmc3 Photon91.0.edm4hep

$K4GenBuildDir/bin/key4HEPAnalysis -i Photon91.0.edm4hep -o Photon91.0.root -p 22,22
