from .GeneratorBase import GeneratorBase
from .PythiaProcDB import PythiaProcDB


class Pythia(GeneratorBase):
    """Pythia class"""

    def __init__(self, procinfo, settings):
        super().__init__(procinfo, settings, "Pythia", "dat")

        self.version = "x.y.z"
        self.file = ""
        self.cuts = ""
        self.PythiaSelectorFileExtension = "selectors"

        self.procDB = PythiaProcDB(self.procinfo)
        if settings.get("usedefaults", True):
            self.procDB.write_DBInfo()

        self.executable = "$K4GenBuildDir/bin/pythiaRunner -f"
        self.gen_settings = settings.get_block("pythia")
        if self.gen_settings is not None:
            self.gen_settings = {k.lower(): v for k, v in self.gen_settings.items()}

        self.selectorsFile = (
            self.GeneratorDatacardBase + "." + self.PythiaSelectorFileExtension
        )
        self.selectorsFileWithPath = self.outdir + "/" + self.selectorsFile
        if settings.get_block("selectors"):
            self.write_selectors()

    def execute(self):
        # prepare the datacard
        self.fill_datacard()
        # prepare the key4hepfile
        self.fill_key4hepScript()

    def fill_datacard(self):
        # prepare the datacard
        self.fill_run()
        self.fill_decay()

    def fill_run(self):
        self.run = ""
        self.add_option("Random:setSeed", "on")
        self.add_option("Random:seed", self.procinfo.get_rndmSeed())

        self.add_option("Beams:eCM", self.procinfo.get("sqrts"))
        beam1_pdg = self.procinfo.get_beam_flavour(1)
        beam2_pdg = self.procinfo.get_beam_flavour(2)

        self.add_option("Beams:idA", beam1_pdg)
        self.add_option("Beams:idB", beam2_pdg)

        if self.procinfo.get("isrmode"):
            self.add_option("PartonLevel:ISR", "on")
            self.add_option("PDF:lepton", "on")
        else:
            self.add_option("PartonLevel:ISR", "off")
            self.add_option("PDF:lepton", "off")
        if self.procinfo.get("fsrmode"):
            self.add_option("PartonLevel:FSR", "on")
        else:
            self.add_option("PartonLevel:FSR", "off")

        self.add_option("Main:numberOfEvents", self.procinfo.get("events"))
        self.run += "\n"
        for p in self.procinfo.get_data_particles():
            for attr in dir(p):
                if not callable(getattr(p, attr)) and not attr.startswith("__"):
                    name = self.is_pythia_particle_data(attr)
                    if name is not None:
                        value = getattr(p, attr)
                        op_name = f"{p.get('pdg_code')}:{name}"
                        if op_name in self.procDB.get_run_out():
                            self.procDB.remove_option(op_name)
                        self.add_option(op_name, value)

        self.add_option("Main:SelectorsFile", self.selectorsFile)

        if "hepmc" in self.procinfo.get("output_format"):
            self.add_option("Main:WriteHepMC", "on")
            outputFile = "{0}.{1}".format(
                self.GeneratorDatacardBase, self.procinfo.get("output_format")
            )
            self.add_option("Main:HepMCFile", outputFile)

        self.run += self.procDB.get_run_out()
        self.run += self.procDB.get_proc_out()

        if self.gen_settings is not None:
            for key, value in self.gen_settings.items():
                self.add_option(key, value)

        self.add2GeneratorDatacard(self.run)

    def fill_decay(self):
        if self.procinfo.get("decay"):
            self.add_decay()

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
            print("Failed to pass process specific cuts in Pythia")
            print(e)
            pass
        for key, value in selectors.items():
            self.add_Selector(value)
        # PYTHIA special: write the selectors to the file proc.selectors
        with open(self.selectorsFileWithPath, "w+") as file:
            file.write(self.cuts)

    def add_Selector(self, value):
        key = value.name.lower()
        if key == "pt":
            self.add_one_ParticleSelector(value, "PT")
        elif key == "et":
            self.add_one_ParticleSelector(value, "ET")
        elif key == "rap":
            self.add_one_ParticleSelector(value, "Rapidity")
        elif key == "eta":
            self.add_one_ParticleSelector(value, "Eta")
        elif key == "theta":
            self.add_one_ParticleSelector(value, "Theta", "rad")

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
            print(f"{key} not a Pythia Selector")

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
            sname = "2 "
            sname += f" {name} {f1} {f2} > {Min}"
            if f" {name} {f1} {f2} >" not in self.cuts:
                self.cuts += sname
                self.cuts += "\n"
            sname = "2 "
            sname += f" {f1} {f2} {name} < {Max}"
            if f"  {f1} {f2} {name} <" not in self.cuts:
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
            sname = "2 "
            sname += f" {name} {f1} {f2} > {Min}"
            if f" {name} {f1} {f2} >" not in self.cuts:
                self.cuts += sname
                self.cuts += "\n"
            sname = "2 "
            sname += f" {f1} {f2} {name} < {Max}"
            if f"  {f1} {f2} {name} <" not in self.cuts:
                self.cuts += sname
                self.cuts += "\n"

    def add_one_ParticleSelector(self, sel, name, unit=""):
        Min, Max = sel.get_MinMax(unit)
        f1 = sel.get_Flavours()
        for f in f1:
            sname = "1 "
            sname += f"{f} {name} > {Min}"
            if f"{f} {name} >" not in self.cuts:
                self.cuts += sname
                self.cuts += "\n"
            sname = "1 "
            sname += f"{f} {name} < {Max}"
            if f"{f} {name} <" not in self.cuts:
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
        # Pythia turn off parent, then turn on
        decays = ""
        for parent in self.procinfo.get_final_pdg_list():
            self.remove_option(f"{parent}:onMode")
            self.remove_option(f"{parent}:onIfAny")
            decays += f"{parent}:onMode off\n"
            child = decay_opt[parent]
            decays += f"{parent}:onIfAny "
            for c in child:
                decays += f"{c} "
            decays += "\n"
        self.add2Datacard("\n")
        self.add2Datacard(decays)

    def fill_key4hepScript(self):
        key4hepRun = ""
        key4hepRun += self.executable + " " + self.GeneratorDatacardName + "\n"

        hepmcformat = self.procinfo.get("output_format")
        key4hepRun += "$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i {0} -o edm4hep {1}.{0} {1}.edm4hep\n".format(
            hepmcformat, self.GeneratorDatacardBase
        )
        self.add2Key4hepScript(key4hepRun)

    def add_option(self, key, value):
        if self.gen_settings is not None:
            if key in self.gen_settings.items():
                value = self.gen_settings.items()[key]
        if key in self.run:
            if str(value) in self.run:
                self.remove_option(key)
            return
        self.run += f"{key} = {value}\n"

    def remove_option(self, opt):
        lines = self.run.split("\n")
        filter_lines = [line for line in lines if opt not in line]
        self.run = "\n".join(filter_lines)

    def is_pythia_particle_data(self, d):
        name = None
        if d == "mass":
            name = "m0"
        if d == "width":
            name = "mWidth"
        return name
