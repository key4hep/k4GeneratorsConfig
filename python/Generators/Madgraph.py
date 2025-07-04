from .GeneratorBase import GeneratorBase
from Particles import Particle as part


class Madgraph(GeneratorBase):
    """Madgraph class"""

    def __init__(self, procinfo, settings):
        super().__init__(procinfo, settings, "Madgraph", "dat")

        self.version = "x.y.z"

        self.add_header()
        self.executable = "mg5_aMC"

        self.setOptionalFileNameAndExtension(f"pythia{self.GeneratorDatacardBase}","cmnd")
        self.fill_PythiaCMND()

    def setSelectorsDict(self):
        # set up the correspondance between the yamlInput and the Sherpa convention
        self.selectorsDict['pt']    = "pt"
        self.selectorsDict['energy']= "e"
        self.selectorsDict['rapidity'] = "eta"
        self.selectorsDict['eta']   = "eta"
        self.selectorsDict['theta'] = "eta"

        self.selectorsDict['mass']     = "mxx"
        self.selectorsDict['angle']     = "Angle"
        self.selectorsDict['deltarapidity'] = "DeltaY"
        self.selectorsDict['deltaphi']      = "DeltaPhi"
        self.selectorsDict['deltar']        = "DeltaR"

    def setModelParameters(self):
        # no alphaS and MZ, these are default
        self.addModelParameter('GFermi')
        #self.addModelParameter('alphaEMMZM1')
        #self.addModelParameter('alphaEMM1')
        # for a coherent setting we need to use a derived value for alphaQED
        #self.addModelParameter('alphaEMEWSchemeM1')
        self.addModelParticleProperty(pdg_code=24, property_type='mass')
        self.addModelParticleProperty(pdg_code=23, property_type='width')
        self.addModelParticleProperty(pdg_code=24, property_type='width')

    def execute(self):
        # prepare the datacard
        self.fill_datacard()
        # prepare the key4hep script
        self.fill_key4hepScript()

    def fill_datacard(self):
        self.addOption2GeneratorDatacard("import model",self.getModel())
        # particles
        self.mg_particles = list(
            map(self.pdg_to_madgraph, self.procinfo.get_particlesOfProcessList())
        )
        self.proc = ""
        for i in range(len(self.mg_particles)):
            self.proc += f"{self.mg_particles[i]} "
            if i == 1:
                self.proc += "> "
        if self.procinfo.get("decay"):
            self.add_decay()
        self.addOption2GeneratorDatacard("generate", self.proc)
        # self.addOption2GeneratorDatacard("output", self.outdir+f"/{self.procinfo.get('procname')}")
        self.addOption2GeneratorDatacard("output", "Output")
        self.addOption2GeneratorDatacard("launch", None)
        self.addOption2GeneratorDatacard("set iseed", self.procinfo.get_rndmSeed())
        self.addOption2GeneratorDatacard("set EBEAM", self.procinfo.get("sqrts") / 2.0)

        # now add the particles checking for overlap with ProcDB
        self.prepareParameters()

        # now add the particles checking for overlap with ProcDB
        self.prepareParticles()
        # temporary fix: increase LHE event size
        self.addOption2GeneratorDatacard("set nevents", int(self.procinfo.get("events")*1.002))
        if self.procinfo.get("isrmode"):
            if self.procinfo.get("beamstrahlung") is not None:
                # if self.gen_settings is None:
                #   print("Please set the beamstrahlung parameter as Madgraph:beamstrahlung:---\n\
                #       Options are: cepc240ll, clic3000ll, fcce240ll, fcce365ll, and ilc500ll.\n\
                #       See arxiv 2108.10261 for more details.")
                #   raise(ValueError)
                # else:
                self.addOption2GeneratorDatacard("set pdlabel", self.get_BeamstrahlungPDLABEL())
            else:
                self.addOption2GeneratorDatacard("set pdlabel", "isronlyll")
            self.addOption2GeneratorDatacard("set lpp1", "3")
            self.addOption2GeneratorDatacard("set lpp2", "-3")
        if any(item != 0. for item in self.procinfo.get_PolarisationFraction()):
            self.addOption2GeneratorDatacard("set polbeam1", 100.*self.procinfo.get_PolarisationDensity()[0]*self.procinfo.get_PolarisationFraction()[0])
            self.addOption2GeneratorDatacard("set polbeam2", 100.*self.procinfo.get_PolarisationDensity()[1]*self.procinfo.get_PolarisationFraction()[1])

        for key in self.procDB.getDict():
            self.addOption2GeneratorDatacard(key, self.procDB.getDict()[key])
        # if self.settings.get_block("selectors"):
        self.writeAllSelectors()
        # else:
        #     self.add_default_Selectors()
        # now the structure is filled, transfer it to the baseclass

    def get_BeamstrahlungPDLABEL(self):
        ecm = self.procinfo.sqrts
        accel = self.procinfo.beamstrahlung.lower()
        # accelerator type is more important than the energy to first order
        if accel == "cepc" or accel == "fcc":
            #
            if ecm < 300:
                 return f"{accel}240ll"
            else:
                 return f"fcc365ll"

        elif accel == "ilc":
            # only one option implemented
            return f"{accel}500ll"

        elif accel == "clic":
            # only one option implemented
            return f"{accel}3000ll"
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
            if str(key) not in self.procinfo.get_finalstate_pdgString():
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

    def add2ParticleSelector2Card(self, sel, name):
        Min, Max = sel.get_MinMax()
        flavs = sel.get_Flavours()
        if len(flavs) == 2:
            f1 = flavs[0]
            f2 = flavs[1]
            if (
                str(f1) not in self.procinfo.get_finalstate_pdgString()
                or str(f2) not in self.procinfo.get_finalstate_pdgString()
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
                    str(f1) not in self.procinfo.get_finalstate_pdgString()
                    or str(f2) not in self.procinfo.get_finalstate_pdgString()
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

                # self.addOption2GeneratorDatacard(sname, maxcut)

    def add1ParticleSelector2Card(self, sel, name):
        # if the unit is deg or rad, we need to change it:
        unit = ""
        if sel.get_unit() == "rad" or sel.get_unit() == "deg":
            unit = "eta"
        Min, Max = sel.get_MinMax(unit)
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
        mincut = f"{{{flav}: {Min}}}"
        self.add2GeneratorDatacard(f"set {sname} {mincut}\n")

        sname = f"{name}_max_pdg"
        maxcut = f"{{{flav}: {Max}}}"
        self.add2GeneratorDatacard(f"set {sname} {maxcut}\n")

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
        outformat = self.procinfo.get_output_format()
        # adding the Pythia step a posteriori if hepmc3 or edm4hep are requested:
        if  outformat == "hepmc3" or outformat == "edm4hep":
            key4hepRun += f"pythiaLHERunner -f {self.getOptionalFileName()} -l unweighted_events.lhe -o {self.GeneratorDatacardBase}.hepmc\n"
            # convert if the highest is requested
            if self.procinfo.get_output_format() == "edm4hep":
                key4hepRun += f"convertHepMC2EDM4HEP -i hepmc3 -o edm4hep {self.GeneratorDatacardBase}.hepmc {self.GeneratorDatacardBase}.edm4hep\n"

        self.add2Key4hepScript(key4hepRun)

    def fill_PythiaCMND(self):
        # append the analysis to the content
        # for the errors allow 1 permil failures
        allowedErrors = int(self.procinfo.get("events")*0.001)
        content  = f"Main:timesAllowErrors = {allowedErrors}\n"
        content += "Check:epTolErr = 0.01\n"
        content += "Main:WriteHepMC = on\n"
        content += "Beams:frameType = 4\n"
        content += "Main:numberOfEvents = {0}\n".format(self.procinfo.get("events"))
        self.add2OptionalFile(content)

    def getModelName(self, model):
        # sm or loop_qcd_qed_sm alphaQED, or loop_qcd_qed_sm_Gmu Gmu,MZ,MW
        # modelDict = { 'sm' : 'sm-full'}
        modelDict = { 'sm' : 'loop_qcd_qed_sm_Gmu-full'}
        if model.lower() not in modelDict.keys():
            print(f"Warning::Madgraph: model {model} has no translation in Madgraph Model Dictionary, using {model}")
            return model
        return modelDict[model.lower()]

    def pdg_to_madgraph(self, particle):
        return particle.get("name")

    def getParameterLabel(self, param):
        parameterDict = { 'GFermi' : 'GF', 'alphaSMZ' : 'aS', 'alphaEMM1' : 'aEWM1' , 'alphaEMEWSchemeM1' : 'aEWM1'}
        # alphas could be SigmaProcess:alphaSvalue
        if param not in parameterDict.keys():
            print(f"Warning::Madgraph: parameter {param} has no translation in Madgraph Parameter Dictionary")
            return ""
        return parameterDict[param]

    def getParameterOperator(self, name):
        return f"set {name}"

    def getGeneratorCommand(self,key,value):
        return f"{key} {value}"

    def getParticleProperty(self, d):
        if d == "mass":
            return "M"
        if d == "width":
            return "W"
        return None

    def getParticleOperator(self, pdg, prop):
        particleName = part.name_from_pdg(int(pdg)).replace("+", "").replace("-", "")
        return f"set {prop}{particleName}"

    def add_header(self):
        self.add2GeneratorDatacard("""#************************************************************
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
#*     run as ./bin/mg5_aMC  filename                       *
#*                                                          *
#************************************************************"\n""")
