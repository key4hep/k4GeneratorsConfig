from .GeneratorBase import GeneratorBase

class Herwig(GeneratorBase):
    """Pythia class"""

    def __init__(self, procinfo):
        super().__init__(procinfo, "Herwig", "in")

        self.version = "x.y.z"

        self.executable = "Herwig"

    def setModelParameters(self):
        # no alphaS and MZ, these are default
        self.addModelParameter('alphaEMM1')
        self.addModelParameter('sin2theta')
        self.addModelParticleProperty(pdg_code=23, property_type='mass')
        self.addModelParticleProperty(pdg_code=23, property_type='width')
        self.addModelParticleProperty(pdg_code=24, property_type='width')

    def execute(self):
        # prepare the datacard
        self.fill_datacard()
        # prepare the key4hep script
        self.fill_key4hepScript()

    def fill_datacard(self):
        # prepare the datacard
        self.fill_run()
        #self.fill_decay()

    def fill_run(self):
        self.addOption2GeneratorDatacard("set Seed", self.procinfo.get_rndmSeed())

        beamA = self.pdg_to_herwig(self.procinfo.get_beam_flavour(1))
        beamB = self.pdg_to_herwig(self.procinfo.get_beam_flavour(2))
        self.addOption2GeneratorDatacard("set EventHandler:BeamA", f"/Herwig/Particles/{beamA}")
        self.addOption2GeneratorDatacard("set EventHandler:BeamB", f"/Herwig/Particles/{beamB}")

        self.add2GeneratorDatacard("cd /Herwig/Generators")
        self.addOption2GeneratorDatacard("set EventGenerator:EventHandler:LuminosityFunction:Energy",self.procinfo.get("sqrts"))

        self.addOption2GeneratorDatacard("set EventGenerator:NumberOfEvents", self.procinfo.settings.get_nevents())
        self.add2GeneratorDatacard("\n")

        # ISR
        if self.procinfo.get("isrmode"):
            self.addOption2GeneratorDatacard("set /Herwig/Shower/SplittingGenerator:ISR", "Yes")
        else:
            self.addOption2GeneratorDatacard("set /Herwig/Shower/SplittingGenerator:ISR", "No")

        # FSR
        if self.procinfo.get("fsrmode"):
            self.addOption2GeneratorDatacard("set /Herwig/Shower/SplittingGenerator:FSR", "Yes")
        else:
            self.addOption2GeneratorDatacard("set /Herwig/Shower/SplittingGenerator:FSR", "No")

        # now add the model parameters
        self.prepareParameters()

        # now add the particles checking for overlap with ProcDB
        self.prepareParticles()

        # add the procDB settings
        for key in self.procDB.getDict():
            value = self.procDB.getDict()[key]
            self.addOption2GeneratorDatacard(key,value)

        # the generator settings from yaml are set last as they superseed all previous settings
        if self.gen_settings is not None:
            for key, value in self.gen_settings.items():
                self.addOption2GeneratorDatacard(key, value)

    def fill_decay(self):
        #if self.procinfo.get("decay"):
            #self.add_decay()
        return

    def fill_key4hepScript(self):
        key4hepRun = ""
        key4hepRun += self.executable + " read " + self.GeneratorDatacardName + "\n"
        key4hepRun += self.executable + " run " + self.GeneratorDatacardBase + ".run\n"

        if self.procinfo.get_output_format() == "edm4hep":
            key4hepRun += f"convertHepMC2EDM4HEP -i hepmc3 -o edm4hep {self.GeneratorDatacardBase}.hepmc3 {self.GeneratorDatacardBase}.edm4hep\n"

        self.add2Key4hepScript(key4hepRun)

    def getGeneratorCommand(self,key,value):
        return f"{key} {value}"

    def getParameterLabel(self, param):
        parameterDict = { 'alphaEMM1' : 'EW/AlphaEM',
                          'sin2theta' : 'EW/Sin2ThetaW',
                          'alphaSMZ' : 'LOAlphaS:input_alpha_s'}
        # alphas could be SigmaProcess:alphaSvalue
        if param not in parameterDict.keys():
            print(f"Warning::Herwig: parameter {param} has no translation in Herwig Parameter Dictionary")
            return ""
        return parameterDict[param]

    def setSelectorsDict(self):
        pass

    def add1ParticleSelector2Card(self, sel, name):
        pass

    def add2ParticleSelector2Card(self, sel, name):
        pass

    def getParameterOperator(self, name):
        return f"set {name}"

    def getParticleProperty(self, d):
        name = None
        if d == "mass":
            name = "Mass"
        if d == "width":
            name = "Width"
        return name

    def getParticleOperator(self, pdg, prop):
        pdgString = self.pdg_to_herwig(abs(int(pdg)), signed=False)
        if pdgString == "Higgs" and prop == "Width":
            pdgString = "h"
        return f"set {pdgString}{prop}"

    def getModelName(self):
        # not needed for Herwig
        pass

    def pdg_to_herwig(self, pdg, signed=True):
        apdg = abs(pdg)
        if type(pdg) is int:
            particle_mapping = {6: "Top", 11: "e", 23: "Z", 25: "Higgs", 24: "W"}
            particle = particle_mapping.get(apdg,"ERROR")
            if not signed:
                return particle
            # continue if we need more
            if particle != "ERROR":
                if apdg <= 6:
                    if pdg > 0:
                        return f"{particle}"
                    else:
                        return f"{particle}bar"
                elif apdg == 11 or apdg == 13 or apdg == 15:
                    if pdg > 0:
                        return f"{particle}-"
                    else:
                        return f"{particle}+"
                elif apdg == 12 or apdg == 14 or apdg == 16:
                    if pdg > 0:
                        return f"{particle}"
                    else:
                        return f"{particle}bar"
                elif apdg == 22 or apdg == 23 or apdg == 25:
                        return f"{particle}"
                elif apdg == 24:
                    if pdg > 0:
                        return f"{particle}+"
                    else:
                        return f"{particle}-"
            else:
                return f"Cant find Herwig id for pdg {pdg}"
