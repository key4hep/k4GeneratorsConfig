from .GeneratorBase import GeneratorBase

class Sherpa(GeneratorBase):
    """Sherpa class"""

    def __init__(self, procinfo, settings):
        super().__init__(procinfo, settings, "Sherpa", "dat")

        self.version = "3"
        self.executable = "Sherpa -f"

    def setSelectorsDict(self):
        # set up the correspondance between the yamlInput and the Sherpa convention
        self.selectorsDict['pt']    = "PT"
        self.selectorsDict['et']    = "ET"
        self.selectorsDict['rapidity'] = "Rapidity"
        self.selectorsDict['eta']   = "Eta"
        self.selectorsDict['theta'] = "Eta"

        self.selectorsDict['mass']     = "Mass"
        self.selectorsDict['angle']    = "Angle"
        self.selectorsDict['deltaeta']      = "DeltaEta"
        self.selectorsDict['deltarapidity'] = "DeltaY"
        self.selectorsDict['deltaphi']      = "DeltaPhi"
        self.selectorsDict['deltar']        = "DeltaR"

    def setModelParameters(self):
        # no alphaS and MZ, these are default
        self.addModelParameter('GFermi')
        self.addModelParticleProperty(pdg_code=23, property_type='mass')
        self.addModelParticleProperty(pdg_code=23, property_type='width')
        self.addModelParticleProperty(pdg_code=24, property_type='width')

    def execute(self):
        # prepare the datacard
        self.fill_datacard()
        # prepare the key4hep script
        self.fill_key4hepScript()

    def write_run(self):
        self.addOption2GeneratorDatacard("RANDOM_SEED", self.procinfo.get_rndmSeed())

        self.addOption2GeneratorDatacard("BEAMS", [self.procinfo.get_beam_flavour(1),self.procinfo.get_beam_flavour(2)])
        self.addOption2GeneratorDatacard("BEAM_ENERGIES", self.procinfo.get("sqrts")/2.)

        self.addOption2GeneratorDatacard("MODEL", self.getModel())

        if self.procinfo.get("isrmode"):
            self.addOption2GeneratorDatacard("PDF_LIBRARY", "PDFESherpa")
        else:
            self.addOption2GeneratorDatacard("PDF_LIBRARY", "None")
        if self.procinfo.get("fsrmode"):
            self.addOption2GeneratorDatacard("YFS_MODE", "FULL")
        else:
            self.addOption2GeneratorDatacard("YFS_MODE", "None")
        self.addOption2GeneratorDatacard("EVENTS", self.procinfo.get("events"))
        self.add2GeneratorDatacard("\n")

        # now add the model checking for overlap
        self.prepareParameters()

        if self.procinfo.get("output_format") == "hepmc2":
            eoutname = "HepMC_GenEvent[{0}]".format(self.GeneratorDatacardBase)
            self.addOption2GeneratorDatacard("EVENT_OUTPUT", eoutname)

        elif self.procinfo.get("output_format") == "hepmc3":
            eoutname = "HepMC3_GenEvent[{0}.hepmc3]".format(self.GeneratorDatacardBase)
            self.addOption2GeneratorDatacard("EVENT_OUTPUT", eoutname)

        # run settings
        for key in self.procDB.getDictParameters():
            self.addOption2GeneratorDatacard(key,self.procDB.getDict()[key])

        self.addOption2GeneratorDatacard("EVENT_GENERATION_MODE", self.procinfo.eventmode)
        if self.gen_settings is not None:
            if "run" in self.gen_settings.keys():
                for key, value in self.gen_settings["run"].items():
                    self.addOption2GeneratorDatacard(key, value)

        # insert the keyword:
        self.add2GeneratorDatacard("\nPARTICLE_DATA:\n")
        # now add the particles checking for overlap with ProcDB
        self.prepareParticles(writeParticleHeader=True)
        self.add2GeneratorDatacard("\n")

    def write_process(self):
        self.add2GeneratorDatacard("\nPROCESSES:\n")
        self.add2GeneratorDatacard(f"- {self.procinfo.get_initial_pdg()} -> {self.procinfo.get_final_pdg()}:\n")
        self.add2GeneratorDatacard(f"    Order: {{QCD: {self.procinfo.get_qcd_order()}, EW: {self.procinfo.get_qed_order()}}}\n")

    def add2ParticleSelector2Card(self, sel, name):
        Min, Max = sel.get_MinMax()
        flavs = sel.get_Flavours()
        if len(flavs) == 2:
            f1 = flavs[0]
            f2 = flavs[1]
            if (
                str(f1) not in self.procinfo.get_final_pdg()
                or str(f2) not in self.procinfo.get_final_pdg()
            ):
                return
            sname = f"  - [{name}, {f1}, {f2}, {Min}, {Max}]"
            if f"  - [{name}, {f1}, {f2}" not in self.getGeneratorDatacard():
                self.add2GeneratorDatacard(f"{sname}\n")
        else:
            for fl in flavs:
                f1 = fl[0]
                f2 = fl[1]
                if (
                    str(f1) not in self.procinfo.get_final_pdg()
                    or str(f2) not in self.procinfo.get_final_pdg()
                ):
                    continue
                sname = f"  - [{name}, {f1}, {f2}, {Min}, {Max}]"
                if f"  - [{name}, {f1}, {f2}" not in self.getGeneratorDatacard():
                    self.add2GeneratorDatacard(f"{sname}\n")

    def add1ParticleSelector2Card(self, sel, name):
        # if the unit is deg or rad, we need to change it:
        unit = ""
        if sel.get_unit() == "rad" or sel.get_unit() == "deg":
            unit = "eta"
        Min, Max = sel.get_MinMax(unit)
        f1 = sel.get_Flavours()
        for f in f1:
            sname = f"  - [{name}, {f}, {Min}, {Max}]"
            if f"  - [{name}, {f}" not in self.getGeneratorDatacard():
                self.add2GeneratorDatacard(f"{sname}\n")

    def write_decay(self):
        # add the header:
        self.add2GeneratorDatacard("\nHARD_DECAYS:\n")
        # Simple check first that parents are
        # in the main process
        decay_opt = self.procinfo.get("decay")
        for key in decay_opt:
            if str(key) not in self.procinfo.get_final_pdg():
                print(
                    "Particle {0} not found in main process. Decay not allowed".format(
                        key
                    )
                )
        # add the channels
        self.add2GeneratorDatacard("  Enabled: true\n")
        self.add2GeneratorDatacard("  Channels:\n")
        for p in self.procinfo.get_final_pdg_list():
            parent = str(p)
            child = decay_opt[p]
            decays = f"    {parent}"
            for c in child:
                decays += f",{c}"
            self.addOption2GeneratorDatacard(decays,"{Status: 2}")

    def fill_datacard(self):
        self.write_run()
        self.write_process()
        # the decay must be written after particles and process, only if the block is set
        if self.procinfo.get("decay"):
            self.write_decay()
        # writing selectors depends on the presence of the block
        if self.settings.get_block("selectors"):
            self.add2GeneratorDatacard("\nSELECTORS:\n")
            self.writeAllSelectors()

    def fill_key4hepScript(self):
        key4hepRun = ""
        if "Amegic" in self.getGeneratorDatacard():
            key4hepRun += self.executable + " " + self.GeneratorDatacardName + "\n"
            key4hepRun += "./makelibs \n"
            key4hepRun += self.executable + " " + self.GeneratorDatacardName + "\n"
        else:
            key4hepRun += self.executable + " " + self.GeneratorDatacardName + "\n"

        hepmcformat = self.procinfo.get("output_format")
        hepmcversion = hepmcformat[-1]
        key4hepRun += "$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i {0} -o edm4hep {1}.hepmc{2} {1}.edm4hep\n".format(
            hepmcformat, self.GeneratorDatacardBase, hepmcversion
        )

        self.add2Key4hepScript(key4hepRun)

    def getModelName(self, model):
        # the model names are from sherpa, so wave through for now
        modelDict = { 'sm' : 'SM'}
        if model.lower() not in modelDict.keys():
            print(f"Warning::Sherpa: model {model} has no translation in Sherpa Model Dictionary, using {model}")
            return model
        return modelDict[model.lower()]

    def getParameterLabel(self, param):
        parameterDict = { 'GFermi' : 'GF', 'alphaSMZ' : 'ALPHAS(MZ)' }
        # alphas could be SigmaProcess:alphaSvalue
        if param not in parameterDict.keys():
            print(f"Warning::Sherpa: parameter {param} has no translation in Sherpa Parameter Dictionary")
            return ""
        return parameterDict[param]

    def getParameterOperator(self, name):
        return f"{name}"

    def getGeneratorCommand(self,key,value):
        return f"{key}: {value}"

    def getParticleProperty(self, d):
        name = None
        d = d.lower()
        if d == "mass":
            name = "Mass"
        if d == "width":
            name = "Width"
        if d == "massive":
            name = "Massive"
        return name

    def getParticleOperator(self, pdg, prop):
        if prop is None:
            return f"  {pdg}"
        return f"    {prop}"

