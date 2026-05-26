# Installation

## Requirements
`Python >= 3.7`
`PyYaml`

Check your python version
```bash
python --version
```

you can install pyYaml as user with:
```bash
pip3 install pyyaml --user
```

## Usage
Before begining, you should setup the environment by:
```bash
source /path/to/k4GeneratorsConfig/setup.(tc)(z)sh
```
The setup script will check that python3 is available on your machine.


## Key4hep

The package is part of Key4hep, to compile the code:
```bash
bash
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
mkdir build
cd build
cmake ../CMakeLists.txt -DCMAKE_INSTALL_PREFIX=../install
make install
cd /path/to/out
./Run_PROCESSNAME.sh
```
⚠️ **Warning**: Always run this scheme as cmake and make set up the environment variables correctly for the execution of the generation step
