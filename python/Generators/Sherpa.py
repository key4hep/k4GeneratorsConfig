import os, stat
import SherpaProcDB

class Sherpa:
    """Sherpa class"""
    def __init__(self, procinfo, settings):
        self.name = "Sherpa"
        self.version = "x.y.z"
        self.procinfo = procinfo
        self.ext = "dat"
        self.file = ""
        self.cuts = ""
        self.yodaout = ""

        self.outdir = f"{procinfo.get('OutDir')}/Sherpa/{self.procinfo.get('procname')}"
        self.outfileName = f"Run_{self.procinfo.get('procname')}"
        self.key4hepfile = f"{self.outdir}/Run_{self.procinfo.get('procname')}"
        self.fullprocname = f"{self.procinfo.get('procname')}"

        if self.procinfo.get("isrmode"):
            self.outfileName += "_ISR"
            self.key4hepfile += "_ISR"
            self.fullprocname += "_ISR"

        self.outfile = f"{self.outdir}/{self.outfileName}"
        self.procDB = SherpaProcDB.SherpaProcDB(self.procinfo)
        self.settings = settings
        if settings.get("usedefaults",True):
            self.procDB.write_DBInfo()

        self.executable  = "Sherpa -f"
        self.gen_settings = settings.get_block("sherpa")
        if self.gen_settings is not None:
            self.gen_settings = {k.lower(): v for k, v in self.gen_settings.items()}
        if settings.get_block("selectors"):
            self.cuts="(selector){\n"
            self.write_selectors()
        try: 
            if settings.get("analysismode").lower()=="rivet":
                self.rivet=True
            if settings.get("yodaoutpath") is not None:
                self.yodaout = getattr(self.settings, "yodaoutpath") + f"/Sherpa_{self.procinfo.get('procname')}.yoda"
            else:
                self.yodaout = f"Sherpa_{self.procinfo.get('procname')}.yoda"
            self.add_rivet()
        except:
            self.rivet=False
            pass

    def write_run(self):
        self.run = "(run){\n"

        self.add_run_option("RANDOM_SEED", self.procinfo.get_rndmSeed())

        ENG = self.procinfo.get("sqrts") / 2.
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
                        
        if  self.procinfo.get("output_format") == "hepmc":
            eoutname="HepMC_GenEvent[{0}]".format(self.fullprocname)
            self.add_run_option("EVENT_OUTPUT", eoutname)
            
        elif self.procinfo.get("output_format") == "hepmc3":
            eoutname="HepMC3_GenEvent[{0}]".format(self.fullprocname)
            self.add_run_option("EVENT_OUTPUT", eoutname)
        self.run += self.procDB.get_run_out()
        self.add_run_option("EVENT_GENERATION_MODE", self.procinfo.eventmode)
        if self.gen_settings is not None:
            if "run" in self.gen_settings.keys():
                for key,value in self.gen_settings["run"].items():
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
            print("Failed to pass process specific cuts in Sherpa")
            print(e)
            pass
        for key,value in selectors.items():
            self.add_Selector(key, value)
        self.cuts+="}(selector)\n"

    def add_Selector(self,key, value):
        key=key.lower()
        if key == "pt":
            self.add_one_ParticleSelector(value, "PT")
        elif key == "et":
            self.add_one_ParticleSelector(value, "ET")
        elif key == "rap":
            self.add_one_ParticleSelector(value, "Rapidity")
        elif key == "eta":
            self.add_one_ParticleSelector(value, "PseudoRapidity")  

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
            print(f"{key} not a Sherpa Selector")

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

    def add_one_ParticleSelector(self,sel,name):
        Min,Max = sel.get_MinMax()
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
        # Sherpa requires the decaying particles get an additional label 25-> 25[a]
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

    def add_rivet(self):
        if  self.procinfo.get("output_format") == "hepmc":
            self.rivethead = f"mkfifo {self.fullprocname}.hepmc2g\n"
        elif self.procinfo.get("output_format") == "hepmc3":
            self.rivethead = f"mkfifo {self.fullprocname}.hepmc3g\n"
        self.rivet_analysis = "rivet"
        for ana in getattr(self.settings,"analyses"):
            self.rivet_analysis += f" -a {ana}"
        for proc, analyses in getattr(self.settings, "procanalyses").items():
            if proc==self.procinfo.get('procname'):
                for ana in analyses:
                    self.rivet_analysis += f" -a {ana}"

        self.rivet_analysis += f" -o {self.yodaout}\n"

    def write_file(self):
        self.write_run()
        self.write_process()
        self.ptext += "}(processes)\n\n"
        self.run += "}(run)\n\n"
        self.file = self.run + self.ptext + self.cuts
        self.outfile += "." + self.ext
        with open(self.outfile, "w+") as file:
            file.write(self.file)

    def write_key4hepfile(self,shell,config):
        key4hepRun = shell+"\n"
        key4hepRun += config+"\n"
        if self.rivet:
            key4hepRun += f'if [ -f "{self.fullprocname}.hepmc"* ]; then\n rm {self.fullprocname}.hepmc*)\n fi\n'
            key4hepRun += self.rivethead
        if "Amegic" in self.file:
            key4hepRun += self.executable+" "+self.outfileName+"."+self.ext+"\n"
            key4hepRun +="./makelibs \n"
            if self.rivet:
                key4hepRun += self.executable+" "+self.outfileName+"."+self.ext+"&\n"
            else:
                key4hepRun += self.executable+" "+self.outfileName+"."+self.ext+"\n"
        else:
            if self.rivet:
                key4hepRun += self.executable+" "+self.outfileName+"."+self.ext+"&\n"
            else:
                key4hepRun += self.executable+" "+self.outfileName+"."+self.ext+"\n" 
        if self.rivet:
            key4hepRun += self.rivet_analysis
        if  self.procinfo.get("output_format") == "hepmc":
            key4hepRun += f"$CONVERTHEPMC2EDM4HEP/convertHepMC2EDM4HEP -i hepmc2 -o edm4hep {self.fullprocname}.hepmc2g {self.fullprocname}.edm4hep\n"
        elif self.procinfo.get("output_format") == "hepmc3":
            key4hepRun += f"$CONVERTHEPMC2EDM4HEP/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep {self.fullprocname}.hepmc3g {self.fullprocname}.edm4hep\n"

        self.key4hepfile += ".sh"
        with open(self.key4hepfile, "w+") as file:
            file.write(key4hepRun)
        os.chmod(self.key4hepfile, os.stat(self.key4hepfile).st_mode | stat.S_IEXEC)

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
