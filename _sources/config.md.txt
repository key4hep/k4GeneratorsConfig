# General Settings
The following are a list of user settings that are common to all event generators. Note that the input key is case-insensitive.

- **Generators**: A list of generators whose runcards should be generated. One generator must be specified
```yaml
Generators:
  - Sherpa
  - Whizard
  - Madgraph

```
- **SqrtS**: $\sqrt{s}$ in GeV.

- **ISRMode**: Enable ISR via electron structure function:
```yaml
ISRMode: 1
```
default: 0 (turned off)

- **OutputFormat**: Format in which the monte-carlo events will be written out to. Currently supported options are hepmc and evx

- **OutDir**: The directory to which the run-cards will be saved. Current default is $PWD/Run-Cards.

- **Events**: Number of Monte-Carlo events to be generated.

- **Processes**: A list of processes which runcards should be generated. Each process should have its own unique name. Under these headings you can
				 specify the final states to be generated and at what order e.g [EW,QCD].
```yaml
Processes:
  Muon:
     Initial: [11, -11]
     Final: [13, -13]
  MuonNeutrino:
     Initial: [11, -11]
     Final: [14, -14]
  Tau:
     Initial: [11, -11]
     Final: [15, -15]
  TauNeutrino:
     Initial: [11, -11]
     Final: [16, -16]
```

- **ParticleData**: Here the user can set various particle properties such as mass and width. Note it is expected of the user to set a consistent input scheme.
					The particles are identified using the corresponding PDG number

```yaml
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
```yaml
PositronPolarisation: 0.3
ElectronPolarisation: 0.8
```
- **Beamstrahlung**: is turned on by specifying the type of accelerator. Allowed values are: ILC, FCC, C3, CEPC, HALFHF.
```yaml
Beamstrahlung: ILC
```
Note that **Beamstrahlung** is conditional on **ISRmode** being on. The **Beamstrahlung** and **SqrtS** variables are used to configure the settings of the generators. For **SqrtS** a vicinity search (within 10GeV) is performed. In case the requested setting does not exist, a replacement setting is used and printed as a warning.

## Analysis
Postgeneration analyses can be performed either using Rivet and/or key4hep
```
Analysis:
  Tools: [key4hep, rivet]
  RivetAnalysis: [MC_XS, MC_ZINC,...]
  RivetPath: /path/to/analysis
```
