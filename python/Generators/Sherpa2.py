from .GeneratorBase import GeneratorBase

class Sherpa2(GeneratorBase):
    """Sherpa2 class"""

    def __init__(self, procinfo, settings):
        super().__init__(procinfo, settings, "Sherpa2", "dat")

        self.version = "2"
        self.executable = "Sherpa -f"

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
        self.add2GeneratorDatacard("(run){\n")

        self.addOption2GeneratorDatacard("RANDOM_SEED", self.procinfo.get_rndmSeed())

        ENG = self.procinfo.get("sqrts") / 2.0
        beam1_pdg = self.procinfo.get_beam_flavour(1)
        beam2_pdg = self.procinfo.get_beam_flavour(2)

        self.addOption2GeneratorDatacard("BEAM_1", beam1_pdg)
        self.addOption2GeneratorDatacard("BEAM_2", beam2_pdg)

        self.addOption2GeneratorDatacard("BEAM_ENERGY_1", ENG)
        self.addOption2GeneratorDatacard("BEAM_ENERGY_2", ENG)
        self.addOption2GeneratorDatacard("MODEL", self.procinfo.get("model"))

        if self.procinfo.get("isrmode"):
            self.addOption2GeneratorDatacard("PDF_LIBRARY", "PDFESherpa")
        else:
            self.addOption2GeneratorDatacard("PDF_LIBRARY", "None")
        if self.procinfo.get("fsrmode"):
            self.addOption2GeneratorDatacard("YFS_MODE", "FULL")
        else:
            self.addOption2GeneratorDatacard("YFS_MODE", "None")
        self.addOption2GeneratorDatacard("EVENTS", self.procinfo.get("events"))
        self.add2GeneratorDatacard("\n\n")

        # now add the model checking for overlap
        self.prepareParameters()

        # now add the particles checking for overlap with ProcDB
        self.prepareParticles()

        if self.procinfo.get("output_format") == "hepmc2":
            eoutname = "HepMC_GenEvent[{0}]".format(self.GeneratorDatacardBase)
            self.addOption2GeneratorDatacard("EVENT_OUTPUT", eoutname)

        elif self.procinfo.get("output_format") == "hepmc3":
            eoutname = "HepMC3_GenEvent[{0}.hepmc3]".format(self.GeneratorDatacardBase)
            self.addOption2GeneratorDatacard("EVENT_OUTPUT", eoutname)

        # run settings
        for key in self.procDB.getDict():
            self.addOption2GeneratorDatacard(key,self.procDB.getDict()[key])
        
        self.addOption2GeneratorDatacard("EVENT_GENERATION_MODE", self.procinfo.eventmode)
        if self.gen_settings is not None:
            if "run" in self.gen_settings.keys():
                for key, value in self.gen_settings["run"].items():
                    self.addOption2GeneratorDatacard(key, value)

    def write_process(self):
        self.add2GeneratorDatacard("(processes){\n")
        if self.procinfo.get("decay"):
            self.add_decay()
        else:
            self.add2GeneratorDatacard(f"  Process {self.procinfo.get_initial_pdg()} -> {self.procinfo.get_final_pdg()};\n")
        self.add2GeneratorDatacard(f"  Order ({self.procinfo.get_qcd_order()},{self.procinfo.get_qed_order()});\n")
        self.add2GeneratorDatacard("  End process;\n")

    def write_selectors(self):
        selectors = getattr(self.settings, "selectors")
        try:
            procselectors = getattr(self.settings, "procselectors")
            for proc, sel in procselectors.items():
                if proc != self.procinfo.get("procname"):
                    continue
                for key, value in sel.items():
                    if value.process == self.procinfo.get("procname"):
                        self.add_Selector(value)
        except Exception as e:
            print("Failed to pass process specific cuts in Sherpa2")
            print(e)
            pass
        for key, value in selectors.items():
            self.add_Selector(value)
        self.add2GeneratorDatacard("}(selector)\n")

    def add_Selector(self, value):
        key = value.name.lower()
        if key == "pt":
            self.add_one_ParticleSelector(value, "PT")
        elif key == "et":
            self.add_one_ParticleSelector(value, "ET")
        elif key == "rap":
            self.add_one_ParticleSelector(value, "Rapidity")
        elif key == "eta":
            self.add_one_ParticleSelector(value, "PseudoRapidity")
        elif key == "theta":
            self.add_one_ParticleSelector(value, "PseudoRapidity", "eta")

            # Two particle selectors
        elif key == "mass":
            self.add_two_ParticleSelector(value, "Mass")
        elif key == "angle":
            self.add_two_ParticleSelector(value, "Angle")
        elif key == "deta":
            self.add_two_ParticleSelector(value, "DeltaEta")
        elif key == "drap":
            self.add_two_ParticleSelector(value, "DeltaY")
        elif key == "dphi":
            self.add_two_ParticleSelector(value, "DeltaPhi")
        elif key == "dr":
            self.add_two_ParticleSelector(value, "DeltaR")
        else:
            print(f"{key} not a Sherpa2 Selector")

    def add_two_ParticleSelector(self, sel, name):
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
            sname = f" {name} {f1} {f2} {Min} {Max}"
            if f" {name} {f1} {f2}" not in self.getGeneratorDatacard():
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
                sname = f" {name} {f1} {f2} {Min} {Max}"
                if f" {name} {f1} {f2}" not in self.getGeneratorDatacard():
                    self.add2GeneratorDatacard(f"{sname}\n")

    def add_one_ParticleSelector(self, sel, name, unit=""):
        Min, Max = sel.get_MinMax(unit)
        f1 = sel.get_Flavours()
        for f in f1:
            sname = f" {name} {f} {Min} {Max}"
            if f" {name} {f}" not in self.getGeneratorDatacard():
                self.add2GeneratorDatacard(f"{sname}\n")

    def add_decay(self):
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
        # Sherpa2 requires the decaying particles get an additional label 25-> 25[a]
        # so parse letters to the process definition
        i = 97
        fs = ""
        decays = ""
        for p in self.procinfo.get_final_pdg_list():
            parent = str(p) + f"[{chr(i)}] "
            child = decay_opt[p]
            fs += parent
            decays += f"  Decay {parent} -> "
            for c in child:
                decays += f"{c} "
            decays += "\n"
            i += 1
        self.add2GeneratorDatacard(f"  Process {self.procinfo.get_initial_pdg()} -> {fs};\n")
        self.add2GeneratorDatacard(decays)

    def fill_datacard(self):
        self.write_run()
        self.add2GeneratorDatacard("}(run)\n\n")
        self.write_process()
        self.add2GeneratorDatacard("}(processes)\n\n")
        if self.settings.get_block("selectors"):
            self.add2GeneratorDatacard("(selector){\n")
            self.write_selectors()

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

    def getParameterLabel(self, param):
        parameterDict = { 'GFermi' : 'GF', 'alphaSMZ' : 'ALPHAS(MZ)' }
        # alphas could be SigmaProcess:alphaSvalue 
        if param not in parameterDict.keys():
            print(f"Warning::Sherpa2: parameter {param} has no translation in Sherpa2 Parameter Dictionary")
            return ""
        return parameterDict[param]

    def getParameterOperator(self, name):
        return f"{name}"

    def getGeneratorCommand(self,key,value):
        return f" {key} {value};"

    def getParticleProperty(self, d):
        name = None
        if d == "mass":
            name = "MASS"
        if d == "width":
            name = "WIDTH"
        return name

    def getParticleOperator(self, part, prop):
        return f"{prop}[{part.get('pdg_code')}]"

