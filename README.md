# k4Generators

## Description
A python based module for the automatic generation of inputfiles for  Monte-Carlo(MC) generators.

## Requirements
`Python >= 3.7`
`PyYaml`  

Check your python version
```
python --version
```

you can install pyYaml as user with:
```
pip3 install pyyaml --user
```

## Usage
Before begining, you should setup the environment by: 
```
source /path/to/k4generators/setup.(tc)(z)sh
```
The setup script will check that python3 is available on your machine.

Once you have written your own inputfile(`input.yaml`), as seen in the [examples](https://gitlab.com/aprice/k4generators/-/tree/main/Examples?ref_type=heads), execute the following:\

`k4gen -f input.yaml`

This will create a directory containing the desired runcards. The directory can be set in the inputfile as:\
`OutDir: /path/to/out`

## Generating events: after the git clone
The commands above create input files for all generators as well as a run script. This run script contains a conversion to the EDM4HEP format. It is therefore necessary to compile the converter provided in this package against the KEY4HEP release you will be using. The first command can be omitted if you are in the BASH shell:
```
bash
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
cd k4Generators
cmake CMakeLists.txt
make
cd /path/to/out
./Run_PROCESSNAME.sh
```

## Generating events: package already installed
For subsequent uses, if you have not modified the C++ code, it is sufficient to setup the environment variables:
```
bash
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
cd k4Generators
source convertHepMC2EDM4HEP_env.sh
cd /path/to/out
./Run_PROCESSNAME.sh
```
