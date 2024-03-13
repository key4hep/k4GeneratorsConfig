# k4GeneratorsConfig

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
source /path/to/k4GeneratorsConfig/setup.(tc)(z)sh
```
The setup script will check that python3 is available on your machine.

Once you have written your own inputfile(`input.yaml`), as seen in the [examples](https://github.com/key4hep/k4GeneratorsConfig/tree/main/examples), execute the following:\

`k4gen -f input.yaml`

This will create a directory containing the desired runcards. The directory can be set in the inputfile as:\
`OutDir: /path/to/out`

## Generating events: after the git clone
The commands above create input files for all generators as well as a run script. This run script contains a conversion to the EDM4HEP format. It is therefore necessary to compile the converter provided in this package against the KEY4HEP release you will be using. The first command can be omitted if you are in the BASH shell:
```
bash
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
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
cd k4GeneratorsConfig
source convertHepMC2EDM4HEP_env.sh
cd /path/to/out
./Run_PROCESSNAME.sh
```


## General Settings
The following are a list of user settings that are common to all event generators. Note that the input key is case-insensitive.

- **Generators**: A list of generators whose runcards should be generated. One generator must be specified
```
		Generators:
		  - Sherpa
		  - Whizard
		  - Madgraph

```
- **SqrtS**: $\sqrt{s}$ in GeV.

- **ISRMode**: Enable ISR via electron structure function:
```
ISRMode: 1 
```
default: 0 (turned off)

- **OutputFormat**: Format in which the monte-carlo events will be written out to. Currently supported options are hepmc and evx

- **OutDir**: The directory to which the run-cards will be saved. Current default is $PWD/Run-Cards.

- **Events**: Number of Monte-Carlo events to be generated.

- **Processes**: A list of processes which runcards should be generated. Each process should have its own unique name. Under these headings you can 
				 specify the final states to be generated and at what order e.g [EW,QCD].
```
		Processes:
		  Muon:
		     Initial: [11, -11]
		     Final: [13, -13]
		     Order: [2,0]
		  MuonNeutrino:
		     Initial: [11, -11]
		     Final: [14, -14]
		     Order: [2,0]
		  Tau:
		     Initial: [11, -11]
		     Final: [15, -15]
		     Order: [2,0]
		  TauNeutrino:
		     Initial: [11, -11]
		     Final: [16, -16]
		     Order: [2,0]


```

- **ParticleData**: Here the user can set various particle properties such as mass and width. Note it is expected of the user to set a consistent input scheme.
					The particles are identified using the corresponding PDG number

```
		ParticleData:
		  25:
		    mass: 125
		    width: 0
		  11:
		    mass: 0.0005111
		    width: 0
		  23:
		    mass: 91.1876
		    width: 2.4952
		  24:
		    mass: 80.379
		    width: 2.085


```

- **Selectors**: Some basic one and two particle phasespace cuts can be set. Each will need to be set with a minimum and maximum value as well as the flavour(s)
				it should be applied to.
  - **One Particle Selectors**:
  	- **PT**: Cut on the transverse momenta
  	- **ETA**: Cut on the pseduorapidity
  	- **Y**: Cut on the Rapidity
  	- **ET**: Cut on the Transverse energy

  - **Two Particle Selectors**:
  	- **Mass**: Cut on the invariant mass of two particles
  	- **Angle**: Cut on the angular separation in radians 
  	- **DEta**: Cut on the pseudorapidity separation
  	- **DY**: Cut on the rapidity separation
  	- **DPhi**: Cut on the azimuthal separation in radians
  	- **DR**: Cut on the R separation


## Generator Specific Settings
Here we summarise the settings available to a subset of generators.


- **Beam Polarization**: Polarized beams are available for Madgraph and Whizard. It can be set as follows
```
		PositronPolarisation: 0.3
		ElectronPolarisation: 0.8
```
- **Beamstrahlung**: is turned on by specifying the type of accelerator. Allowed values are: ILC, FCC, C3, CEPC, HALFHF.
```
Beamstrahlung: ILC
```
Note that **Beamstrahlung** is conditional on **ISRmode** being on. The **Beamstrahlung** and **SqrtS** variables are used to configure the settings of the generators. For **SqrtS** a vicinity search (within 10GeV) is performed. In case the requested setting does not exist, a replacement setting is used and printed as a warning.
