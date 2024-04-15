from GeneratorBase import GeneratorBase
import Particles
import WhizardProcDB

class Whizard(GeneratorBase):
    """Whizard class"""
    def __init__(self, procinfo, settings):
        super().__init__(procinfo, settings,"Whizard","sin")

        self.version = "x.y.z"
        self.file = ""
        self.cuts = ""
        self.integrate = ""

        self.procDB = WhizardProcDB.WhizardProcDB(self.procinfo)
        if settings.get("usedefaults",True):
            self.procDB.write_DBInfo()

        self.executable  = "whizard"
        self.gen_settings = settings.get_block("whizard")
        if self.gen_settings is not None:
            self.gen_settings = {k.lower(): v for k, v in self.gen_settings.items()}

        self.procs = []

    def write_process(self):
        self.whiz_beam1 = self.pdg_to_whizard(self.procinfo.get_beam_flavour(1))
        self.whiz_beam2 = self.pdg_to_whizard(self.procinfo.get_beam_flavour(2))
        self.finalstate = ", ".join(map(self.pdg_to_whizard, self.procinfo.get_final_pdg_list()))

        try:
            if "model" in self.gen_settings:
                self.process = f'model = {self.gen_settings["model"]}\n'
        except:
            self.process = f"model = {self.procinfo.get('model')}\n"

        self.add_process_option("seed",self.procinfo.get_rndmSeed())

        if self.procinfo.get("isrmode"):
            self.add_process_option("?isr_handler", "true")
            self.process += f"beams = {self.whiz_beam1}, {self.whiz_beam2}"
            # insert circe
            if self.procinfo.Beamstrahlung is not None:
                self.process += f" => circe2 "
            self.process += f" => isr,isr\n"
            isrmass = 0.000511
            self.add_process_option("isr_mass", isrmass)
            # insert the circe file
            if self.procinfo.Beamstrahlung is not None:
                self.process += f"$circe_file= \"{self.procinfo.get_BeamstrahlungFile()}\"\n"
        else:
            self.add_process_option("?isr_handler", "false")

        if self.procinfo.get_ElectronPolarisation()!=0 or self.procinfo.get_PositronPolarisation()!=0:
            self.process += f"beams_pol_density = @({self.procinfo.get_PolDensity()[0]}), @({self.procinfo.get_PolDensity()[1]})\n"
            self.process += f"beams_pol_fraction = {self.procinfo.get_ElectronPolarisation()}, {self.procinfo.get_PositronPolarisation()}\n"

        self.process += f"process proc = {self.whiz_beam1}, {self.whiz_beam2} => {self.finalstate}\n"

        self.add_process_option("n_events", self.procinfo.get("events"))
        self.add_process_option("sqrts", self.procinfo.get("sqrts"))
        if self.procinfo.get("decay"):
            self.add_decay()

        for p in self.procinfo.get_data_particles():
            for attr in dir(p):
                if not callable(getattr(p, attr)) and not attr.startswith("__"):
                    name = self.is_whizard_particle_data(attr)
                    if name is not None:
                        value = getattr(p, attr)
                        pname = self.pdg_to_whizard(p.get("pdg_code"))
                        if p.get("pdg_code") < 20:
                            pname = pname.lower()
                            if abs(p.get("pdg_code")) == 6:
                                pname = "top"
                        replac = ["+", "-", "1", "2", "3"]
                        for r in replac:
                            pname = pname.replace(r, "")
                        if name == "MASS":
                            dname = f"m{pname}"
                        elif name == "WIDTH":
                            dname = f"w{pname}"
                        self.add_process_option(dname, value)

        # output format only hepm2 or hepmc3, the actual version is detected by the linked library, so strip the number
        self.add_process_option("sample_format", str(self.procinfo.get("output_format")).rstrip("23"))
        self.add_process_option("?hepmc_output_cross_section","true")
        self.add_process_option("?write_raw","false")
        self.process += self.procDB.get_run_out()
        if self.procinfo.eventmode == "unweighted":
            self.add_process_option("?unweighted", "true")
        else:
            self.add_process_option("?unweighted", "false")
        if self.settings.get_block("selectors"):
            self.cutsadded = False
            self.write_selectors()

    def add_decay(self):
        decay_opt = self.procinfo.get("decay")
        decays=""
        for key in decay_opt:
            parent = self.pdg_to_whizard(key)
            decays += f"process decay{parent} = {parent} => "
            for child in decay_opt[key]:
                if child is decay_opt[key][-1]:
                    decays += self.pdg_to_whizard(child) + ""
                else:
                    decays += self.pdg_to_whizard(child) + ", "

            decays +="\n"
            decays +=f"unstable {parent} (decay{parent})\n"
            # decays +=f"integrate (decay{parent})\n"
            self.procs.append(f"decay{parent}")

        self.process += decays

    def write_selectors(self):
        self.cuts = "cuts = "
        selectors = getattr(self.settings,"selectors")
        try:
            procselectors = getattr(self.settings, "procselectors")
            for proc, sel in procselectors.items():
                    for key, value in sel.items():
                        if key.startswith(self.procinfo.get('procname')):
                            # print(key,proc)
                            cut = key.split(proc)
                            if len(cut)==2:
                                self.add_Selector(cut[1], value)
        except Exception as e:
            print("Failed to pass process specific cuts in Whizard")
            print(e)
            pass
        for key,value in selectors.items():
            self.add_Selector(key, value)

    def add_Selector(self,key, value):
        key=key.lower()
        if key == "pt":
            self.add_one_ParticleSelector(value, "Pt")
        elif key == "energy":
            self.add_one_ParticleSelector(value, "E")
        elif key == "rap":
            self.add_one_ParticleSelector(value, "rap")
        elif key == "eta":
            self.add_one_ParticleSelector(value, "eta")
            # Two particle selectors
        elif key == "mass":
            self.add_two_ParticleSelector(value,"m")
        else:
            print(f"{key} not a Standard Whizard Selector")


    def add_two_ParticleSelector(self,sel,name):
        Min,Max = sel.get_MinMax()
        flavs = sel.get_Flavours()
        if len(flavs) == 2:
            f1 = self.pdg_to_whizard(flavs[0])
            f2 = self.pdg_to_whizard(flavs[1])
            if str(f1) not in self.finalstate or str(f2) not in self.finalstate:
                return
            if self.cutsadded is False:
                self.cuts+=f" all {Min} < {name} <= {Max} [{f1},{f2}] \n"
                self.cutsadded = True
            else:
                self.cuts+=f" and all {Min} < {name} <= {Max} [{f1},{f2}] \n"

        else:
            for fl in flavs:
                f1 = self.pdg_to_whizard(fl[0])
                f2 = self.pdg_to_whizard(fl[1])
                if str(f1) not in self.finalstate or str(f2) not in self.finalstate:
                    continue
                if self.cutsadded is False:
                    self.cuts+=f" all {Min} < {name} <= {Max} [{f1},{f2}] \n"
                    self.cutsadded = True
                else:
                    self.cuts+=f" and all {Min} < {name} <= {Max} [{f1},{f2}] \n"

    def add_one_ParticleSelector(self,sel,name):
        Min,Max = sel.get_MinMax()
        f1 = sel.get_Flavours()
        for f in f1:
            f=self.pdg_to_whizard(f)
            if self.cutsadded is False:
                self.cuts+=f" all {Min} < {name} <= {Max} [{f}] \n"
                self.cutsadded = True
            else:
                self.cuts+=f" and all {Min} < {name} <= {Max} [{f}] \n"


    def write_integrate(self):
        for p in self.procs:
            self.integrate += f"integrate ({p})\n"
        self.integrate += "simulate (proc) { iterations = 5:5000}\n"

    def add_process_option(self, key, value):
        if key in self.process:
            print(f"{key} has already been defined in {self.name}.")
            return
        if f"{key}" in self.procDB.get_run_out():
            self.procDB.remove_option(key)
        self.process += f"{key} = {value}\n"

    def write_file(self):
        self.write_process()
        if self.cuts != "cuts = ":
            self.process += self.cuts
        self.process += "compile\n"
        self.write_integrate()
        self.file = f"{self.process}{self.integrate}"
        self.write_GeneratorDatacard(self.file)

    def write_key4hepfile(self):
        key4hepRun = ""
        key4hepRun += self.executable+" "+self.GeneratorDatacardName+"\n"
        key4hepRun += "$CONVERTHEPMC2EDM4HEP/convertHepMC2EDM4HEP -i {0} -o edm4hep proc.hepmc {1}.edm4hep\n".format(self.procinfo.get("output_format"),self.GeneratorDatacardBase)
        self.write_Key4hepScript(key4hepRun)

    def is_whizard_particle_data(self, d):
        name = None
        if d == "mass":
            name = "MASS"
        if d == "width":
            name = "WIDTH"
        return name

    def pdg_to_whizard(self, pdg):
        apdg = abs(pdg)
        if type(pdg) is int:
            if 11 <= apdg <= 16:
                lepton_type = "e" if pdg%2==1 else "n"
                flavor = (apdg - 11) // 2 + 1
                if pdg < 0:
                    lepton_type=lepton_type.capitalize() 
                return f"{lepton_type}{flavor}"
            elif apdg > 20:
                particle_mapping = {23: "Z", 25: "H", 24: "W-", -24: "W+"}
                return particle_mapping.get(pdg, f"Cant find whizard id for pdg {pdg}")
            elif apdg <= 6:
                return self.whizard_quarks(pdg)
            else:
                return f"Cant find whizard id for pdg {pdg}"

    def whizard_quarks(self, pdg):
        quark_mapping = {1: "d", 2: "u", 3: "s", 4: "c", 5: "b", 6: "t"}
        q = quark_mapping.get(abs(pdg), "")
        return q.capitalize() if pdg > 0 else q
