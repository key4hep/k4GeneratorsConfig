from GeneratorBase import GeneratorBase
import BabayagaProcDB


class Babayaga(GeneratorBase):
    """Babayaga class"""

    def __init__(self, procinfo, settings):
        super().__init__(procinfo, settings, "Babayaga", "dat")

        self.version = "x.y.z"
        self.file = ""
        self.process = ""
        self.cuts = ""

        self.procDB = BabayagaProcDB.BabayagaProcDB(self.procinfo)
        if settings.get("usedefaults", True):
            self.procDB.write_DBInfo()

        self.executable = "babayaga-fcc.exe"
        self.gen_settings = settings.get_block("babayaga")
        if self.gen_settings is not None:
            self.gen_settings = {k.lower(): v for k, v in self.gen_settings.items()}

        self.procs = []

    def write_process(self):
        if (
            abs(self.procinfo.get_beam_flavour(1)) != 11
            or abs(self.procinfo.get_beam_flavour(1)) != 11
        ):
            print(
                f"Babayaga not implemented for initial state {self.babayaga_beam1} {self.babayaga_beam2}"
            )
            return

        finalstate = self.procinfo.get_final_pdg().split(" ")
        self.finalstate = "".join(map(self.pdg_to_babayaga, finalstate))
        self.process = f"fs {self.finalstate}\n"

        self.add_process_option("seed", self.procinfo.get_rndmSeed())

        # overwrite if the variable nlo requests qed:
        if self.procinfo.get_nlo().lower() == "lo":
            self.add_process_option("ord", "born")
            self.add_process_option("EWKc", "off")
        elif self.procinfo.get_nlo().lower() == "qed":
            self.add_process_option("ord", "alpha")
            self.add_process_option("EWKc", "on")

        self.add_process_option("nev", self.procinfo.get("events"))
        self.add_process_option("ecms", self.procinfo.get("sqrts"))

        # output format only hepm2 or hepmc3, the actual version is detected by the linked library, so strip the number
        self.add_process_option("store", "yes")
        self.add_process_option("path", ".")
        self.process += self.procDB.get_run_out()
        if self.procinfo.eventmode == "unweighted":
            self.add_process_option("mode", "unweighted")
        else:
            self.add_process_option("mode", "weighted")

        if self.settings.get_block("selectors"):
            self.write_selectors()

    def add_decay(self):
        print("DECAY specified, cannot be implmented in Babayaga")

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
            print("Failed to pass process specific cuts in Babayaga")
            print(e)
            pass
        for key, value in selectors.items():
            self.add_Selector(value)

    def add_Selector(self, value):
        key = value.name.lower()
        if key == "theta":
            self.add_one_ParticleSelector(value, "theta", "deg")
        else:
            print(f"{key} not a Standard Babayaga Selector")

    def add_one_ParticleSelector(self, sel, name, unit=""):
        Min, Max = sel.get_MinMax(unit)
        if name == "theta":
            self.cuts += f"thmin {Min}\n"
            self.cuts += f"thmax {Max}\n"

    def add_process_option(self, key, value):
        if key in self.process:
            print(f"{key} has already been defined in {self.name}.")
            return
        if f"{key}" in self.procDB.get_run_out():
            self.procDB.remove_option(key)
        self.process += f"{key} {value}\n"

    def write_file(self):
        self.write_process()
        self.file = self.process + self.cuts
        # last command is run
        self.file += "run\n"
        self.write_GeneratorDatacard(self.file)

    def write_key4hepfile(self):
        key4hepRun = ""
        key4hepRun += (
            "cat " + self.GeneratorDatacardName + " | " + self.executable + "\n"
        )
        key4hepRun += "$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i lhe -o {0} events.lhe {1}.{0}\n".format(
            self.procinfo.get("output_format"), self.GeneratorDatacardBase
        )
        key4hepRun += "$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i {0} -o edm4hep {1}.{0} {1}.edm4hep\n".format(
            self.procinfo.get("output_format"), self.GeneratorDatacardBase
        )
        self.write_Key4hepScript(key4hepRun)

    def pdg_to_babayaga(self, pdg):
        apdg = abs(int(pdg))
        if type(apdg) is int:
            if apdg == 11 or apdg == 13 or apdg == 22:
                particle_mapping = {11: "e", 13: "m", 22: "g"}
                return particle_mapping.get(
                    apdg, f"Cant find babayaga id for pdg {pdg}"
                )
            else:
                return f"Cant find babayaga id for pdg {pdg}"
