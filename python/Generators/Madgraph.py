from .GeneratorBase import GeneratorBase
from Particles import Particle as part


class Madgraph(GeneratorBase):
    """Madgraph class"""

    def __init__(self, procinfo, settings):
        super().__init__(procinfo, settings, "Madgraph", "dat")

        self.version = "x.y.z"

        self.add_header()
        self.executable = "mg5_aMC"

    def execute(self):
        # prepare the datacard
        self.fill_datacard()
        # prepare the key4hep script
        self.fill_key4hepScript()

    def fill_datacard(self):
        try:
            if "model" in self.gen_settings:
                self.add_option("import model", self.gen_settings["model"].lower())
        except:
            self.add_option("import model", self.procinfo.get("model").lower())
        self.mg_particles = list(
            map(self.pdg_to_madgraph, self.procinfo.get_particles())
        )
        self.proc = ""
        for i in range(len(self.mg_particles)):
            self.proc += f"{self.mg_particles[i]} "
            if i == 1:
                self.proc += "> "
        if self.procinfo.get("decay"):
            self.add_decay()
        self.add_option("generate", self.proc)
        # self.add_option("output", self.outdir+f"/{self.procinfo.get('procname')}")
        self.add_option("output", "Output")
        self.add_option("launch", None)
        self.add_option("set iseed", self.procinfo.get_rndmSeed())
        self.add_option("set EBEAM", self.procinfo.get("sqrts") / 2.0)

        # now add the particles checking for overlap with ProcDB
        self.prepareParticles()

        self.add_option("set nevents", self.procinfo.get("events"))
        if self.procinfo.get("isrmode"):
            if self.procinfo.get("beamstrahlung") is not None:
                # if self.gen_settings is None:
                #   print("Please set the beamstrahlung parameter as Madgraph:beamstrahlung:---\n\
                #       Options are: cepc240ll, clic3000ll, fcce240ll, fcce365ll, and ilc500ll.\n\
                #       See arxiv 2108.10261 for more details.")
                #   raise(ValueError)
                # else:
                self.add_option("set pdlabel", self.get_BeamstrahlungPDLABEL())
                # self.GeneratorDatacard += f"_{self.get_BeamstrahlungPDLABEL()}"
                # self.key4hepfile += f"{self.get_BeamstrahlungPDLABEL()}"
            else:
                self.add_option("set pdlabel", "isronlyll")
            self.add_option("set lpp1", "3")
            self.add_option("set lpp2", "-3")
        if self.procinfo.get_ElectronPolarisation() != 0 or self.procinfo.get_PositronPolarisation()!= 0:
            self.add_option("set polbeam1", self.procinfo.get_ElectronPolarisation()*100.)
            self.add_option("set polbeam2", self.procinfo.get_PositronPolarisation()*100.)
        self.run += self.procDB.get_run_out()
        # if self.settings.get_block("selectors"):
        self.write_selectors()
        # else:
        #     self.add_default_Selectors()
        # now the structure is filled, transfer it to the baseclass
        self.add2GeneratorDatacard(self.run)

    def get_BeamstrahlungPDLABEL(self):
        ecm = self.procinfo.sqrts
        accel = self.procinfo.beamstrahlung
        if abs(ecm - 240) < 10:
            if accel.lower() == "cepc":
                return f"{accel.lower()}240ll"
            elif accel.lower() == "fcc":
                return f"{accel.lower()}e240ll"
            else:
                print(
                    "No setting found for requested accelerator " + accel + "using FCCE"
                )
                return "fcce240ll"
        elif abs(ecm - 365) < 10:
            if accel.lower() == "fcc":
                return f"{accel.lower()}365ll"
            else:
                print(
                    "No setting found for requested accelerator " + accel + "using FCCE"
                )
                return "fcc365ll"
        elif abs(ecm - 500) < 10:
            if accel.lower() == "ilc":
                return f"{accel.lower()}500ll"
            else:
                print(
                    "No setting found for requested accelerator " + accel + "using ILC"
                )
                return "ilc500ll"
        elif abs(ecm - 3000) < 10:
            if accel.lower() == "clic":
                return f"{accel.lower()}3000ll"
            else:
                print(
                    "No setting found for requested accelerator " + accel + "using CLIC"
                )
                return "clic3000ll"
        else:
            print(
                f"No Beamstrahlung setting available for MADGRAPH at this energy {ecm}"
            )
            print("Using ILC at 500GeV")
            return "ilc500ll"

    def add_decay(self):
        # Simple check first that parents are
        # in the main process
        decay_opt = self.procinfo.get("decay")
        decays = " "
        for key in decay_opt:
            if str(key) not in self.procinfo.get_final_pdg():
                print(
                    "Particle {0} not found in main process. Decay not allowed".format(
                        key
                    )
                )
            parent = part.name_from_pdg(key)
            decays += f", {parent} > "
            for child in decay_opt[key]:
                decays += f"{part.name_from_pdg(child)} "
        self.proc += decays

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
            print("Failed to pass process specific cuts in Madgraph")
            print(e)
            pass
        for key, value in selectors.items():
            self.add_Selector(value)

    def add_Selector(self, value):
        key = value.name.lower()
        if key == "pt":
            self.add_one_ParticleSelector(value, "pt")
        elif key == "energy":
            self.add_one_ParticleSelector(value, "e")
        elif key == "rap":
            self.add_one_ParticleSelector(value, "eta")
        elif key == "eta":
            self.add_one_ParticleSelector(value, "eta")
        elif key == "theta":
            self.add_one_ParticleSelector(value, "eta", "eta")

            # Two particle selectors
        elif key == "mass":
            self.add_two_ParticleSelector(value, "mxx")
        elif key == "angle":
            self.add_two_ParticleSelector(value, "Angle")
        elif key == "deta":
            self.add_two_ParticleSelector(value, "Angle")
        elif key == "drap":
            self.add_two_ParticleSelector(value, "DeltaY")
        elif key == "dphi":
            self.add_two_ParticleSelector(value, "DeltaPhi")
        elif key == "dr":
            self.add_two_ParticleSelector(value, "DeltaR")
        else:
            print(f"{key} not a MadGraph Selector")

    def add_two_ParticleSelector(self, sel, name, flavs=None):
        Min, Max = sel.get_MinMax()
        if not flavs:
            flavs = sel.get_Flavours()
        if len(flavs) == 2:
            f1 = flavs[0]
            f2 = flavs[1]
            if (
                str(f1) not in self.procinfo.get_final_pdg()
                or str(f2) not in self.procinfo.get_final_pdg()
            ):
                return
            self.add_min_max_cut(f1, name, Min, Max)
            # sname = f"{name}_min_pdg"
            # mincut = f"{f}: {Min}"
            # self.run+=f"set {sname} {mincut}\n"
            # sname = f"{name}_max_pdg"
            # maxcut = f"{f}: {Max}"
            # self.run+=f"set {sname} {maxcut}\n"

        else:
            for fl in flavs:
                f1 = fl[0]
                f2 = fl[1]
                if (
                    str(f1) not in self.procinfo.get_final_pdg()
                    or str(f2) not in self.procinfo.get_final_pdg()
                ):
                    continue
                if f1 != -f2:
                    print("Cannot set cuts in MadGraph this way.")
                self.add_min_max_cut(f1, name, Min, Max)
                # sname = f"{name}_min_pdg"
                # mincut = f"{f1}: {Min}"
                # self.run+=f"set {sname} {mincut}\n"

                # sname = f"{name}_max_pdg"
                # maxcut = f"{f1}: {Max}"
                # self.run+=f"set {sname} {maxcut}\n"

                # self.add_option(sname, maxcut)

    def add_one_ParticleSelector(self, sel, name, unit="", f1=None):
        Min, Max = sel.get_MinMax(unit)
        if not f1:
            f1 = sel.get_Flavours()
        for f in f1:
            if f < 0:
                continue
            self.add_min_max_cut(f, name, Min, Max)
            # sname = f"{name}_min_pdg"
            # mincut = f"{f}: {Min}"
            # self.run+=f"set {sname} {mincut}\n"

            # sname = f"{name}_max_pdg"
            # maxcut = f"{f}: {Max}"
            # self.run+=f"set {sname} {maxcut}\n"

    def add_min_max_cut(self, flav, name, Min, Max):
        sname = f"{name}_min_pdg"
        mincut = f"{flav}: {Min}"
        self.run += f"set {sname} {mincut}\n"

        sname = f"{name}_max_pdg"
        maxcut = f"{flav}: {Max}"
        self.run += f"set {sname} {maxcut}\n"

    def write_file(self):
        self.fill_run()
        self.write_GeneratorDatacard(self.run)

    def fill_key4hepScript(self):
        key4hepRun = ""
        key4hepRun += self.executable + " " + self.GeneratorDatacardName + "\n"
        # now the running part temporarily on LHE
        key4hepRun += "gunzip Output/Events/run_01/unweighted_events.lhe.gz\n"
        key4hepRun += (
            f"ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe\n"
        )
        # adding the Pythia step a poetriori
        pythiaFile = "pythia"+self.GeneratorDatacardBase+".cmnd"
        self.write_PythiaCMND(pythiaFile)
        key4hepRun += "$K4GenBuildDir/bin/pythiaLHERunner -f {0} -l unweighted_events.lhe -o {1}.hepmc\n".format(
            pythiaFile,self.GeneratorDatacardBase
        )
        # temporarily kick out the header since the
        #key4hepRun += "sed -i '/<header>/,/<\/header>/{//!d}' unweighted_events.lhe\n"
        #key4hepRun += f"$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i lhe -o hepmc3 unweighted_events.lhe {self.GeneratorDatacardBase}.hepmc\n"
        hepmcformat = self.procinfo.get("output_format")
        key4hepRun += "$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i {0} -o edm4hep {1}.hepmc {1}.edm4hep\n".format(
            hepmcformat, self.GeneratorDatacardBase
        )
        self.add2Key4hepScript(key4hepRun)

    def write_PythiaCMND(self, pythiaFile):
        # append the analysis to the content
        content  = "Main:timesAllowErrors = 5\n"
        content += "Main:WriteHepMC = on\n"
        content += "Beams:frameType = 4\n"
        content += "Main:numberOfEvents = {0}\n".format(self.procinfo.get("events"))

        # open the file for the evgen generation in EDM4HEP format
        with open(self.outdir + "/"+pythiaFile, "w+") as file:
            # the generator specific part
            file.write(content)

    def add_option(self, key, value):
        if key in self.run:
            print(f"{key} has already been defined in {self.name}.")
            return
        if value is not None:
            self.run += f"{key} {value}\n"
        else:
            self.run += f"{key}\n"

    def pdg_to_madgraph(self, particle):
        return particle.get("name")

    def formatLine(self,key,value):
        return f"{key} {value}"

    def is_particle_data(self, d):
        if d == "mass":
            return "M"
        if d == "width":
            return "W"
        return None

    def get_particle_operator(self, part, prop):
        particleName = part.get("name").replace("+", "").replace("-", "")
        return f"set {prop}{particleName}"

    def add_header(self):
        self.run = """#************************************************************
#*                        MadGraph 5                        *
#*                                                          *
#*                *                       *                 *
#*                  *        * *        *                   *
#*                    * * * * 5 * * * *                     *
#*                  *        * *        *                   *
#*                *                       *                 *
#*                                                          *
#*                                                          *
#*    The MadGraph Development Team - Please visit us at    *
#*    https://server06.fynu.ucl.ac.be/projects/madgraph     *
#*                                                          *
#************************************************************
#*                                                          *
#*               Command File for MadGraph 5                *
#*                                                          *
#*     run as ./bin/mg5  filename                           *
#*                                                          *
#************************************************************"\n"""
