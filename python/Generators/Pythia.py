from .GeneratorBase import GeneratorBase

class Pythia(GeneratorBase):
    """Pythia class"""

    def __init__(self, procinfo, settings):
        super().__init__(procinfo, settings, "Pythia", "dat")

        self.version = "x.y.z"

        self.executable = "pythiaRunner -f"

        self.setOptionalFileNameAndExtension(self.GeneratorDatacardBase,"selectors")
        if settings.get_block("selectors"):
            self.writeAllSelectors()

    def setSelectorsDict(self):
        # set up the correspondance between the yamlInput and the Sherpa convention
        self.selectorsDict['pt']    = "PT"
        self.selectorsDict['et']    = "ET"
        self.selectorsDict['rapidity']   = "Rapidity"
        self.selectorsDict['eta']   = "Eta"
        self.selectorsDict['theta'] = "Theta"

        self.selectorsDict['mass']     = "Mass"
        self.selectorsDict['angle']    = "Angle"
        self.selectorsDict['deltaeta']      = "DeltaEta"
        self.selectorsDict['deltarapidity'] = "DeltaY"
        self.selectorsDict['deltaphi']      = "DeltaPhi"
        self.selectorsDict['deltar']        = "DeltaR"

    def setModelParameters(self):
        # no alphaS and MZ, these are default
        self.addModelParameter('alphaEMMZ')
        self.addModelParameter('GFermi')
        self.addModelParameter('sin2theta')
        self.addModelParameter('sin2thetaEff')
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
        self.fill_decay()

    def fill_run(self):
        self.addOption2GeneratorDatacard("Random:setSeed", "on")
        self.addOption2GeneratorDatacard("Random:seed", self.procinfo.get_rndmSeed())

        self.addOption2GeneratorDatacard("Beams:eCM", self.procinfo.get("sqrts"))
        beam1_pdg = self.procinfo.get_beam_flavour(1)
        beam2_pdg = self.procinfo.get_beam_flavour(2)

        self.addOption2GeneratorDatacard("Beams:idA", beam1_pdg)
        self.addOption2GeneratorDatacard("Beams:idB", beam2_pdg)

        if self.procinfo.get("isrmode"):
            self.addOption2GeneratorDatacard("PartonLevel:ISR", "on")
            self.addOption2GeneratorDatacard("PDF:lepton", "on")
        else:
            self.addOption2GeneratorDatacard("PartonLevel:ISR", "off")
            self.addOption2GeneratorDatacard("PDF:lepton", "off")
        if self.procinfo.get("fsrmode"):
            self.addOption2GeneratorDatacard("PartonLevel:FSR", "on")
        else:
            self.addOption2GeneratorDatacard("PartonLevel:FSR", "off")

        self.addOption2GeneratorDatacard("Main:numberOfEvents", self.procinfo.get("events"))
        self.add2GeneratorDatacard("\n")

        # now add the model parameters
        self.prepareParameters()

        # now add the particles checking for overlap with ProcDB
        self.prepareParticles()

        self.addOption2GeneratorDatacard("Main:SelectorsFile", self.getOptionalFileName())

        outformat = self.procinfo.get_output_format()
        if  outformat == "hepmc3" or outformat == "edm4hep":
            self.addOption2GeneratorDatacard("Main:WriteHepMC", "on")
            outputFile = "{0}.hepmc3".format(
                self.GeneratorDatacardBase
            )
            self.addOption2GeneratorDatacard("Main:HepMCFile", outputFile)

        # add the procDB settings
        for key in self.procDB.getDict():
            value = self.procDB.getDict()[key]
            self.addOption2GeneratorDatacard(key,value)

        # the generator settings from yaml are set last as they superseed all previous settings
        if self.gen_settings is not None:
            for key, value in self.gen_settings.items():
                self.addOption2GeneratorDatacard(key, value)


    def fill_decay(self):
        if self.procinfo.get("decay"):
            self.add_decay()

    def add2ParticleSelector2Card(self, sel, name):
        Min, Max = sel.get_MinMax()
        flavs = sel.get_Flavours()
        if len(flavs) == 2:
            f1 = flavs[0]
            f2 = flavs[1]
            if (
                str(f1) not in self.procinfo.get_finalstate_pdgString()
                or str(f2) not in self.procinfo.get_finalstate_pdgString()
            ):
                return

            sname = f"2 {name} {f1} {f2} > {Min}"
            if f" {name} {f1} {f2} >" not in self.getOptionalFileContent():
                self.add2OptionalFile(f"{sname}\n")

            sname = f"2 {f1} {f2} {name} < {Max}"
            if f"  {f1} {f2} {name} <" not in self.getOptionalFileContent():
                self.add2OptionalFile(f"{sname}\n")
        else:
            for fl in flavs:
                f1 = fl[0]
                f2 = fl[1]
                if (
                    str(f1) not in self.procinfo.get_finalstate_pdgString()
                    or str(f2) not in self.procinfo.get_finalstate_pdgString()
                ):
                    continue

            sname = f"2 {name} {f1} {f2} > {Min}"
            if f" {name} {f1} {f2} >" not in self.getOptionalFileContent():
                self.add2OptionalFile(f"{sname}\n")

            sname = f"2 {f1} {f2} {name} < {Max}"
            if f"  {f1} {f2} {name} <" not in self.cuts:
                self.cuts += f"{sname}\n"

    def add1ParticleSelector2Card(self, sel, name):
        # if the unit is deg or rad, we need to change it:
        unit = ""
        if sel.get_unit() == "rad" or sel.get_unit() == "deg":
            unit = "rad"
        Min, Max = sel.get_MinMax(unit)
        f1 = sel.get_Flavours()

        for f in f1:
            sname = f"1 {f} {name} > {Min}"
            if f"{f} {name} >" not in self.getOptionalFileContent():
                self.add2OptionalFile(f"{sname}\n")

            sname = f"1 {f} {name} < {Max}"
            if f"{f} {name} <" not in self.getOptionalFileContent():
                self.add2OptionalFile(f"{sname}\n")

    def add_decay(self):
        # Simple check first that parents are
        # in the main process
        decay_opt = self.procinfo.get("decay")
        for key in decay_opt:
            if str(key) not in self.procinfo.get_finalstate_pdgString():
                print(
                    "Particle {0} not found in main process. Decay not allowed".format(
                        key
                    )
                )
        # Pythia turn off parent, then turn on
        decays = ""
        for parent in self.procinfo.get_finalstate_pdgDictList():
            self.removeOptionGeneratorDatacard(f"{parent}:onMode")
            self.removeOptionGeneratorDatacard(f"{parent}:onIfAny")
            decays += f"{parent}:onMode off\n"
            child = decay_opt[parent]
            decays += f"{parent}:onIfAny "
            for c in child:
                decays += f"{c} "
            decays += "\n"
        self.add2GeneratorDatacard("\n")
        self.add2GeneratorDatacard(decays)

    def fill_key4hepScript(self):
        key4hepRun = ""
        key4hepRun += self.executable + " " + self.GeneratorDatacardName + "\n"

        if self.procinfo.get_output_format() == "edm4hep":
            key4hepRun += f"convertHepMC2EDM4HEP -i hepmc3 -o edm4hep {self.GeneratorDatacardBase}.hepmc3 {self.GeneratorDatacardBase}.edm4hep\n"

        self.add2Key4hepScript(key4hepRun)

    def getGeneratorCommand(self,key,value):
        return f"{key} = {value}"

    def getParameterLabel(self, param):
        parameterDict = { 'alphaEMMZ' : 'alphaEMmZ', 'GFermi' : 'GF',
                          'sin2theta' : 'sin2thetaW', 'sin2thetaEff': 'sin2thetaWbar',
                          'alphaSMZ' : 'alphaSvalueMRun'}
        # alphas could be SigmaProcess:alphaSvalue
        if param not in parameterDict.keys():
            print(f"Warning::Pythia: parameter {param} has no translation in Pythia Parameter Dictionary")
            return ""
        return parameterDict[param]

    def getParameterOperator(self, name):
        if "alphaS" not in name:
            return f"StandardModel:{name}"
        else:
            return f"ParticleData:{name}"
        # return f"SigmaProcess:{name}"

    def getParticleProperty(self, d):
        name = None
        if d == "mass":
            name = "m0"
        if d == "width":
            name = "mWidth"
        return name

    def getParticleOperator(self, pdg, prop):
        return f"{pdg}:{prop}"

