from .GeneratorBase import GeneratorBase

class Babayaga(GeneratorBase):
    """Babayaga class"""

    def __init__(self, procinfo, settings):
        super().__init__(procinfo, settings, "Babayaga", "dat")

        self.version = "x.y.z"

        self.cuts = ""

        self.executable = "babayaga-fcc.exe"

    def setSelectorsDict(self):
        # set up the correspondance between the yamlInput and the Sherpa convention
        self.selectorsDict['theta'] = "Theta"

    def execute(self):
        # prepare the datacard
        self.fill_datacard()
        # prepare the key4hep script
        self.fill_key4hepScript()

    def setModelParameters(self):
        # nothing to be set
        return

    def write_process(self):
        if (
            abs(self.procinfo.get_beam_flavour(1)) != 11
            or abs(self.procinfo.get_beam_flavour(2)) != 11
        ):
            print(
                f"Babayaga not implemented for initial state {self.procinfo.get_beam_flavour(1)} {self.procinfo.get_beam_flavour(2)}"
            )
            return

        self.finalstate = "".join(map(self.pdg_to_babayaga, self.procinfo.get_finalstate_pdgList()))
        self.add2GeneratorDatacard(f"fs {self.finalstate}\n")

        self.addOption2GeneratorDatacard("seed", self.procinfo.get_rndmSeed())

        # overwrite if the variable nlo requests qed:
        if self.procinfo.get_nlo().lower() == "lo":
            self.addOption2GeneratorDatacard("ord", "born")
            self.addOption2GeneratorDatacard("EWKc", "off")
        elif self.procinfo.get_nlo().lower() == "qed":
            self.addOption2GeneratorDatacard("ord", "alpha")
            self.addOption2GeneratorDatacard("EWKc", "on")

        self.addOption2GeneratorDatacard("nev", self.procinfo.get("events"))
        self.addOption2GeneratorDatacard("ecms", self.procinfo.get("sqrts"))

        # output format only hepm2 or hepmc3, the actual version is detected by the linked library, so strip the number
        self.addOption2GeneratorDatacard("store", "yes")
        self.addOption2GeneratorDatacard("path", ".")

        # procDB
        for key in self.procDB.getDict():
            self.addOption2GeneratorDatacard(key,self.procDB.getDict()[key])

        if self.procinfo.eventmode == "unweighted":
            self.addOption2GeneratorDatacard("mode", "unweighted")
        else:
            self.addOption2GeneratorDatacard("mode", "weighted")

        if self.settings.get_block("selectors"):
            self.writeAllSelectors()

    def add_decay(self):
        print("DECAY specified, cannot be implmented in Babayaga")

    def add1ParticleSelector2Card(self, sel, name):
        if name == "Theta":
            unit = "deg"
            Min, Max = sel.get_MinMax(unit)
            self.cuts += f"thmin {Min}\n"
            self.cuts += f"thmax {Max}\n"
        else:
            print(f"{key} is a not implemented as selector in {self.name}")

    def fill_datacard(self):
        self.write_process()
        self.add2GeneratorDatacard(self.cuts)
        # last command is run
        self.add2GeneratorDatacard("run\n")

    def fill_key4hepScript(self):
        key4hepRun = ""
        key4hepRun += (
            "cat " + self.GeneratorDatacardName + " | " + self.executable + "\n"
        )
        key4hepRun += "{0}/convertHepMC2EDM4HEP -i lhe -o {1} events.lhe {2}.{1}\n".format(
            self.binDir, self.procinfo.get("output_format"), self.GeneratorDatacardBase
        )
        key4hepRun += "{0}/convertHepMC2EDM4HEP -i {1} -o edm4hep {2}.{1} {2}.edm4hep\n".format(
            self.binDir, self.procinfo.get("output_format"), self.GeneratorDatacardBase
        )
        self.add2Key4hepScript(key4hepRun)

    def getGeneratorCommand(self,key,value):
        return f"{key} {value}"

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
