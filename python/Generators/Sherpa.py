from .GeneratorBase import GeneratorBase

class Sherpa(GeneratorBase):
    """Sherpa class"""

    def __init__(self, procinfo, settings):
        super().__init__(procinfo, settings, "Sherpa", "dat")

        self.version = "x.y.z"
        self.file = ""
        self.cuts = ""

        self.executable = "Sherpa -f"

        if settings.get_block("selectors"):
            self.cuts = "(selector){\n"
            self.write_selectors()

    def execute(self):
        # prepare the datacard
        self.fill_datacard()
        # prepare the key4hep script
        self.fill_key4hepScript()
        
    def write_run(self):
        self.run = "(run){\n"

        self.add_run_option("RANDOM_SEED", self.procinfo.get_rndmSeed())

        ENG = self.procinfo.get("sqrts") / 2.0
        beam1_pdg = self.procinfo.get_beam_flavour(1)
        beam2_pdg = self.procinfo.get_beam_flavour(2)

        self.add_run_option("BEAM_1", beam1_pdg)
        self.add_run_option("BEAM_2", beam2_pdg)

        self.add_run_option("BEAM_ENERGY_1", ENG)
        self.add_run_option("BEAM_ENERGY_2", ENG)
        self.add_run_option("MODEL", self.procinfo.get("model"))

        if self.procinfo.get("isrmode"):
            self.add_run_option("PDF_LIBRARY", "PDFESherpa")
        else:
            self.add_run_option("PDF_LIBRARY", "None")
        if self.procinfo.get("fsrmode"):
            self.add_run_option("YFS_MODE", "FULL")
        else:
            self.add_run_option("YFS_MODE", "None")
        self.add_run_option("EVENTS", self.procinfo.get("events"))
        self.run += "\n\n"
        for p in self.procinfo.get_data_particles():
            for attr in dir(p):
                if not callable(getattr(p, attr)) and not attr.startswith("__"):
                    name = self.is_sherpa_particle_data(attr)
                    if name is not None:
                        value = getattr(p, attr)
                        op_name = f"{name}[{p.get('pdg_code')}]"
                        if op_name in self.procDB.get_run_out():
                            self.procDB.remove_option(op_name)
                        self.add_run_option(op_name, value)
        if self.procinfo.get("output_format") == "hepmc2":
            eoutname = "HepMC_GenEvent[{0}]".format(self.GeneratorDatacardBase)
            self.add_run_option("EVENT_OUTPUT", eoutname)

        elif self.procinfo.get("output_format") == "hepmc3":
            eoutname = "HepMC3_GenEvent[{0}.hepmc3]".format(self.GeneratorDatacardBase)
            self.add_run_option("EVENT_OUTPUT", eoutname)
        self.run += self.procDB.get_run_out()
        self.add_run_option("EVENT_GENERATION_MODE", self.procinfo.eventmode)
        if self.gen_settings is not None:
            if "run" in self.gen_settings.keys():
                for key, value in self.gen_settings["run"].items():
                    self.add_run_option(key, value)

    def write_process(self):
        self.ptext = "(processes){\n"
        if self.procinfo.get("decay"):
            self.add_decay()
        else:
            self.ptext += f"  Process {self.procinfo.get_initial_pdg()} -> {self.procinfo.get_final_pdg()};\n"
        self.ptext += f"  Order ({self.procinfo.get_qcd_order()},{self.procinfo.get_qed_order()});\n"
        self.ptext += "  End process;\n"

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
            print("Failed to pass process specific cuts in Sherpa")
            print(e)
            pass
        for key, value in selectors.items():
            self.add_Selector(value)
        self.cuts += "}(selector)\n"

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
            print(f"{key} not a Sherpa Selector")

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
            if f" {name} {f1} {f2}" not in self.cuts:
                self.cuts += sname
                self.cuts += "\n"
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
                if f" {name} {f1} {f2}" not in self.cuts:
                    self.cuts += sname
                    self.cuts += "\n"

    def add_one_ParticleSelector(self, sel, name, unit=""):
        Min, Max = sel.get_MinMax(unit)
        f1 = sel.get_Flavours()
        for f in f1:
            sname = f" {name} {f} {Min} {Max}"
            if f" {name} {f}" not in self.cuts:
                self.cuts += sname
                self.cuts += "\n"

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
        # Sherpa requires the decaying particles get an additional label 25-> 25[a]
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
        self.ptext += f"  Process {self.procinfo.get_initial_pdg()} -> {fs};\n"
        self.ptext += decays

    def fill_datacard(self):
        self.write_run()
        self.write_process()
        self.ptext += "}(processes)\n\n"
        self.run += "}(run)\n\n"
        self.file = self.run + self.ptext + self.cuts
        self.add2GeneratorDatacard(self.file)

    def fill_key4hepScript(self):
        key4hepRun = ""
        if "Amegic" in self.file:
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

    def add_run_option(self, key, value):
        if self.gen_settings is not None:
            if "run" in self.gen_settings.keys():
                if key in self.gen_settings["run"]:
                    value = self.gen_settings["run"][key]
        if key in self.run:
            if str(value) in self.run:
                return
            print(f"{key} has already been defined in {self.name} with value.")
            return
        self.run += f" {key} {value};\n"

    def add_process_option(self, key, value):
        if key in self.ptext:
            print(f"{key} has already been defined in {self.name}.")
            return
        self.ptext += f" {key} {value};\n"

    def is_sherpa_particle_data(self, d):
        name = None
        if d == "mass":
            name = "MASS"
        if d == "width":
            name = "WIDTH"
        return name
