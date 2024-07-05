from GeneratorBase import GeneratorBase
import PythiaProcDB

class Pythia(GeneratorBase):
    """Pythia class"""
    def __init__(self, procinfo, settings):
        super().__init__(procinfo, settings,"Pythia","dat")

        self.version = "x.y.z"
        self.file = ""
        self.cuts = ""

        self.procDB = PythiaProcDB.PythiaProcDB(self.procinfo)
        if settings.get("usedefaults",True):
            self.procDB.write_DBInfo()

        self.executable  = "$PYTHIA8RUNNER/pythiaRunner -f"
        self.gen_settings = settings.get_block("pythia")
        if self.gen_settings is not None:
            self.gen_settings = {k.lower(): v for k, v in self.gen_settings.items()}
        if settings.get_block("selectors"):
            print("Pythia Warning: selectors not yet implemented")
            #self.write_selectors()

    def write_run(self):

        self.run=""
        self.add_run_option("Random:setSeed", "on")
        self.add_run_option("Random:seed", self.procinfo.get_rndmSeed())

        self.add_run_option("Beams:eCM",self.procinfo.get("sqrts"))
        beam1_pdg = self.procinfo.get_beam_flavour(1)
        beam2_pdg = self.procinfo.get_beam_flavour(2)

        self.add_run_option("Beams:idA", beam1_pdg)
        self.add_run_option("Beams:idB", beam2_pdg)

        if self.procinfo.get("isrmode"):
            self.add_run_option("PartonLevel:ISR", "on")
        else:
            self.add_run_option("PartonLevel:ISR", "off")

        self.add_run_option("Main:numberOfEvents", self.procinfo.get("events"))
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
                        self.add_run_option(op_name, value)

        if  "hepmc" in self.procinfo.get("output_format"):
            self.add_run_option("Main:WriteHepMC", "on")
            self.add_run_option("Main:HepMCFile",self.GeneratorDatacardName)
        
        self.run += self.procDB.get_run_out()
        self.run += self.procDB.get_proc_out()

        if self.gen_settings is not None:
            if "run" in self.gen_settings.keys():
                for key,value in self.gen_settings["run"].items():
                    self.add_run_option(key, value)

    def write_decay(self):
        if self.procinfo.get("decay"):
            print("Pythia Warning: Decay not yet implemented")
            #self.add_decay()

    def write_selectors(self):
        selectors = getattr(self.settings,"selectors")
        try:
            procselectors = getattr(self.settings, "procselectors")
            for proc, sel in procselectors.items():
                if proc != self.procinfo.get('procname'):
                    continue
                for key, value in sel.items():
                    if value.process==self.procinfo.get('procname'):
                        self.add_Selector(value)
        except Exception as e:
            print("Failed to pass process specific cuts in Pythia")
            print(e)
            pass
        for key,value in selectors.items():
            self.add_Selector(value)
        self.cuts+="}(selector)\n"

    def add_Selector(self,value):
        key=value.name.lower()
        if key == "pt":
            self.add_one_ParticleSelector(value, "PT")
        elif key == "et":
            self.add_one_ParticleSelector(value, "ET")
        elif key == "rap":
            self.add_one_ParticleSelector(value, "Rapidity")
        elif key == "eta":
            self.add_one_ParticleSelector(value, "PseudoRapidity")  
        elif key == "theta":
            self.add_one_ParticleSelector(value, "PseudoRapidity","eta")  

            # Two particle selectors
        elif key == "mass":
            self.add_two_ParticleSelector(value,"Mass")
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

    def add_two_ParticleSelector(self,sel,name):
        Min,Max = sel.get_MinMax()
        flavs = sel.get_Flavours()
        if len(flavs) == 2:
            f1 = flavs[0]
            f2 = flavs[0]
            if str(f1) not in self.procinfo.get_final_pdg() or str(f2) not in self.procinfo.get_final_pdg():
                return
            sname = f" {name} {f1} {f2} {Min} {Max}"
            if f" {name} {f1} {f2}" not in self.cuts:
                self.cuts+=sname
                self.cuts+="\n"
        else:
            for fl in flavs:
                f1 = fl[0]
                f2 = fl[1]
                if str(f1) not in self.procinfo.get_final_pdg() or str(f2) not in self.procinfo.get_final_pdg():
                    continue
                sname = f" {name} {f1} {f2} {Min} {Max}"
                if f" {name} {f1} {f2}" not in self.cuts:
                    self.cuts+=sname
                    self.cuts+="\n"

    def add_one_ParticleSelector(self,sel,name,unit=""):
        Min,Max = sel.get_MinMax(unit)
        f1 = sel.get_Flavours()
        for f in f1:
            sname = f" {name} {f} {Min} {Max}"
            if f" {name} {f}" not in self.cuts:
                self.cuts+=sname
                self.cuts+="\n"



    def add_decay(self):
        # Simple check first that parents are 
        # in the main process
        decay_opt = self.procinfo.get("decay")
        for key in decay_opt:
            if str(key) not in self.procinfo.get_final_pdg():
                print("Particle {0} not found in main process. Decay not allowed".format(key))
        # Pythia requires the decaying particles get an additional label 25-> 25[a]
        # so parse letters to the process definition
        i = 97
        fs=""
        decays=""
        for p in self.procinfo.get_final_pdg_list():
            parent = str(p) + f"[{chr(i)}] "
            child = decay_opt[p]
            fs += parent
            decays += f"  Decay {parent} -> "
            for c in child: 
                decays += f"{c} "
            decays+="\n"  
            i+=1
        self.ptext += f"  Process {self.procinfo.get_initial_pdg()} -> {fs};\n"
        self.ptext += decays

		

    def write_file(self):
        self.write_run()
        self.write_decay()
        self.file = self.run + self.cuts
        self.write_GeneratorDatacard(self.file)

    def write_key4hepfile(self):
        key4hepRun = ""
        key4hepRun += self.executable+" "+self.GeneratorDatacardName+"\n"

        hepmcformat = self.procinfo.get("output_format")
        key4hepRun += "$CONVERTHEPMC2EDM4HEP/convertHepMC2EDM4HEP -i {0} -o edm4hep {1}.hepmc {1}.edm4hep\n".format(hepmcformat,self.GeneratorDatacardBase)

        self.write_Key4hepScript(key4hepRun)

    def add_run_option(self, key, value):
        if self.gen_settings is not None:
            if "run" in self.gen_settings.keys():
                if key in self.gen_settings["run"]:
                    value = self.gen_settings["run"][key]
        if key in self.run:
            if str(value) in self.run:
                return
            return
        self.run += f"{key} = {value}\n"

    def add_process_option(self, key, value):
        if key in self.ptext:
            print(f"{key} has already been defined in {self.name}.")
            return
        self.ptext += f"{key} = {value}\n"

    def is_pythia_particle_data(self, d):
        name = None
        if d == "mass":
            name = "m0"
        if d == "width":
            name = "mWidth"
        return name
