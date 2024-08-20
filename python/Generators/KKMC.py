from GeneratorBase import GeneratorBase
import KKMCProcDB
import os, sys


class KKMC(GeneratorBase):
    """KKMC class"""

    def __init__(self, procinfo, settings):
        super().__init__(procinfo, settings, "KKMC", "dat")

        self.version = "x.y.z"
        self.file = ""
        self.process = ""
        self.cuts = ""

        self.procDB = KKMCProcDB.KKMCProcDB(self.procinfo)
        if settings.get("usedefaults", True):
            self.procDB.write_DBInfo()

        self.executable = "KKMC-fcc.exe"
        self.gen_settings = settings.get_block("kkmc")
        if self.gen_settings is not None:
            self.gen_settings = {k.lower(): v for k, v in self.gen_settings.items()}

        self.procs = []
        # Load default settigns
        defaultfile = os.path.dirname(__file__) + "/.KKMCDefaults"
        with open(defaultfile, "r") as file:
            self.defaults = file.read()

    def write_process(self):
        if (
            abs(self.procinfo.get_beam_flavour(1)) != 11
            or abs(self.procinfo.get_beam_flavour(1)) != 11
        ):
            print(
                f"KKMC not implemented for initial state {self.KKMC_beam1} {self.KKMC_beam2}"
            )
            return

        finalstate = self.procinfo.get_final_pdg().split(" ")
        if len(finalstate) != 2:
            print("WARNING: KKMC is only for e+e- -> f fbar")
            sys.exit()
        if abs(int(finalstate[0])) != abs(int(finalstate[1])):
            print(f"WARNING: Final states {finalstate} not allowed in KKMC")
            sys.exit()
        self.finalstate = self.pdg_to_KKMC(finalstate[0])
        self.add_process_option("_seed", self.procinfo.get_rndmSeed())
        self.add_process_option("_energy", self.procinfo.get("sqrts"))
        self.add_process_option("_besdelta", 0)
        # TODO add bes
        self.add_process_option("_besmode", 0)
        self.add_process_option("_ewmode", self.procinfo.get("ewmode"))
        self.add_process_option("_isrmode", self.procinfo.get("isrmode"))
        self.add_process_option("_fsrmode", self.settings.get("fsrmode", 0))
        self.add_final_State()

        # output format only hepm2 or hepmc3, the actual version is detected by the linked library, so strip the number
        if self.procinfo.eventmode == "unweighted":
            self.add_process_option("_wgtmode", "0")
        else:
            self.add_process_option("_wgtmode", "1")

    def add_decay(self):
        print("DECAY specified, cannot be implmented in KKMC")

    def add_final_State(self):
        fs = f"  {self.finalstate}              1"
        self.add_process_option("_FINALSTATES", fs)

    def add_process_option(self, key, value):
        if not isinstance(value, str):
            value = str(value)
        if key in self.process:
            print(f"{key} has already been defined in {self.name}.")
            return
        if f"{key}" in self.procDB.get_run_out():
            self.procDB.remove_option(key)
        if key in self.defaults:
            self.defaults = self.defaults.replace(key, value)
        else:
            print(f"Warning: {key} not set as defaults in KKCM. Ignoring")

    def write_file(self):
        self.write_process()
        self.write_GeneratorDatacard(self.defaults)

    def write_key4hepfile(self):
        key4hepRun = ""
        key4hepRun += "KKMCee -c  {0} -o {1}.{2}\n".format(
            self.GeneratorDatacardName,
            self.GeneratorDatacardBase,
            self.procinfo.get("output_format"),
        )
        key4hepRun += "$K4GENERATORSCONFIG/convertHepMC2EDM4HEP -i {0} -o edm4hep {1}.{0} {1}.edm4hep\n".format(
            self.procinfo.get("output_format"), self.GeneratorDatacardBase
        )
        self.write_Key4hepScript(key4hepRun)

    def pdg_to_KKMC(self, pdg):
        apdg = abs(400 + int(pdg))
        return f"{apdg}"
