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

Once you have written your own inputfile(`input.yaml`), as seen in the [examples](https://github.com/key4hep/k4GeneratorsConfig/tree/main/examples), execute the following:

```
k4GeneratorsConfig input.yaml
```

This will create a directory containing the desired runcards. The directory can be set in the inputfile as:
```yaml
OutDir: /path/to/out
```

## Generating events: after the git clone
The commands above create input files for all generators as well as a run script. This run script contains a conversion to the EDM4HEP format. It is therefore necessary to compile the converter provided in this package against the KEY4HEP release you will be using. The first command can be omitted if you are in the BASH shell:
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
