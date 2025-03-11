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

mg5_aMC MuonNeutrino91.2_ISR.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
$K4GenBuildDir/bin/pythiaLHERunner -f pythiaMuonNeutrino91.2_ISR.cmnd -l unweighted_events.lhe -o MuonNeutrino91.2_ISR.hepmc
$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep MuonNeutrino91.2_ISR.hepmc MuonNeutrino91.2_ISR.edm4hep

$K4GenBuildDir/bin/analyze2f -a 14 -b -14 -i MuonNeutrino91.2_ISR.edm4hep -o MuonNeutrino91.2_ISR.root
