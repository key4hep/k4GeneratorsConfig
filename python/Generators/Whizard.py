from .GeneratorBase import GeneratorBase

class Whizard(GeneratorBase):
    """Whizard class"""

    def __init__(self, procinfo, settings):
        super().__init__(procinfo, settings, "Whizard", "sin")

        self.version = "x.y.z"

        self.executable = "whizard"

        self.procs = []

    def setSelectorsDict(self):
        # set up the correspondance between the yamlInput and the Sherpa convention
        self.selectorsDict['pt']    = "Pt"
        self.selectorsDict['energy']= "E"
        self.selectorsDict['rap']   = "rap"
        self.selectorsDict['eta']   = "eta"
        self.selectorsDict['theta'] = "theta"

        self.selectorsDict['mass']     = "m"

    def setModelParameters(self):
        # no alphaS and MZ, these are default
        self.addModelParameter('GFermi')
        self.addModelParticleProperty(pdg_code=23, property_type='mass')
        self.addModelParticleProperty(pdg_code=23, property_type='width')
        self.addModelParticleProperty(pdg_code=24, property_type='width')

    def execute(self):
        # prepare the datacard
        self.fill_datacard()
        # prepare the key4hep script
        self.fill_key4hepScript()

    def write_process(self):
        self.whiz_beam1 = self.pdg_to_whizard(self.procinfo.get_beam_flavour(1))
        self.whiz_beam2 = self.pdg_to_whizard(self.procinfo.get_beam_flavour(2))
        fsParticles = [int(pdg) for pdg in self.procinfo.get_final_pdg().split(" ")]
        self.finalstate = ", ".join(
            map(self.pdg_to_whizard, fsParticles)
        )

        self.addOption2GeneratorDatacard("model", self.getModel())
        self.addOption2GeneratorDatacard("seed", self.procinfo.get_rndmSeed())

        if self.procinfo.get("isrmode"):
            self.addOption2GeneratorDatacard("?isr_handler", "true")
            self.add2GeneratorDatacard(f"beams = {self.whiz_beam1}, {self.whiz_beam2}")
            # insert circe
            if self.procinfo.get("beamstrahlung") is not None:
                self.add2GeneratorDatacard(f" => circe2 ")
            self.add2GeneratorDatacard(f" => isr,isr\n")
            isrmass = 0.000511
            self.addOption2GeneratorDatacard("isr_mass", isrmass)
            # insert the circe file and turn off polarization if necessary
            if self.procinfo.get("beamstrahlung") is not None:
                self.add2GeneratorDatacard(
                    f'$circe2_file= "{self.procinfo.get_BeamstrahlungFile()}"\n'
                )
                # guinea pig cannot do polarization, so we have to set it to false, but we should be prepared....
                if all(item == 0. for item in self.procinfo.get_PolarisationFraction()):
                    self.add2GeneratorDatacard(f"?circe2_polarized= false\n")
                else:
                    self.add2GeneratorDatacard(f"?circe2_polarized= false\n")
        else:
            self.addOption2GeneratorDatacard("?isr_handler", "false")

        if any(item != 0. for item in self.procinfo.get_PolarisationFraction()):
            self.add2GeneratorDatacard(f"beams_pol_density = @({self.procinfo.get_PolarisationDensity()[0]}), @({self.procinfo.get_PolarisationDensity()[1]})\n")
            self.add2GeneratorDatacard(f"beams_pol_fraction = {self.procinfo.get_PolarisationFraction()[0]}, {self.procinfo.get_PolarisationFraction()[1]}\n")

        self.add2GeneratorDatacard(f"process proc = {self.whiz_beam1}, {self.whiz_beam2} => {self.finalstate}\n")

        self.addOption2GeneratorDatacard("n_events", self.procinfo.get("events"))
        self.addOption2GeneratorDatacard("sqrts", self.procinfo.get("sqrts"))
        if self.procinfo.get("decay"):
            self.add_decay()

        # now add the model checking for overlap
        self.prepareParameters()

        # now add the particles checking for overlap with ProcDB
        self.prepareParticles()

        # output format only hepm2 or hepmc3, the actual version is detected by the linked library, so strip the number
        self.addOption2GeneratorDatacard(
            "sample_format", str(self.procinfo.get("output_format")).rstrip("23")
        )
        self.addOption2GeneratorDatacard("?hepmc_output_cross_section", "true")
        self.addOption2GeneratorDatacard("?write_raw", "false")

        for key in self.procDB.getDict():
            self.addOption2GeneratorDatacard(key,self.procDB.getDict()[key])

        if self.procinfo.eventmode == "unweighted":
            self.addOption2GeneratorDatacard("?unweighted", "true")
        else:
            self.addOption2GeneratorDatacard("?unweighted", "false")

        if self.settings.get_block("selectors"):
            self.CutKeyWdPresent = False
            self.aCutIsPresent   = False
            self.write_selectors()

    def add_decay(self):
        decay_opt = self.procinfo.get("decay")
        decays = ""
        for key in decay_opt:
            parent = self.pdg_to_whizard(key)
            decays += f"process decay{parent} = {parent} => "
            for child in decay_opt[key]:
                if child is decay_opt[key][-1]:
                    decays += self.pdg_to_whizard(child) + ""
                else:
                    decays += self.pdg_to_whizard(child) + ", "

            decays += "\n"
            decays += f"unstable {parent} (decay{parent})\n"
            # decays +=f"integrate (decay{parent})\n"
            self.procs.append(f"decay{parent}")

        self.add2GeneratorDatacard(decays)

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
            print("Failed to pass process specific cuts in Whizard")
            print(e)
            pass
        for key, value in selectors.items():
            self.add_Selector(value)

    def add_Selector(self, select):
        # get the native key for the selector
        try: 
            key = self.selectorsDict[select.name.lower()]
        except:
            print(f"{key} cannot be translated into a Whizard selector")
            print(f"Ignoring the selector")
            return

        # add the selector implementation
        if select.NParticle == 1:
            # if the unit is deg or rad, we need to change it:
            unit = ""
            if select.get_unit() == "deg":
                unit = "rad"
            self.add_one_ParticleSelector(select, key, unit)
        elif select.NParticle == 2:
            self.add_two_ParticleSelector(select, key)
        else:
            print(f"{key} is a {select.NParticle} Particle selector, not implemented in Whizard")

    def add_two_ParticleSelector(self, sel, name):
        Min, Max = sel.get_MinMax()
        flavs = sel.get_Flavours()
        if len(flavs) == 2:
            f1 = self.pdg_to_whizard(flavs[0])
            f2 = self.pdg_to_whizard(flavs[1])
            if str(f1) not in self.finalstate or str(f2) not in self.finalstate:
                return
            self.addCut2GeneratorDatacard(" all {Min} < {name} <= {Max} [{f1},{f2}] \n")
        else:
            for fl in flavs:
                f1 = self.pdg_to_whizard(fl[0])
                f2 = self.pdg_to_whizard(fl[1])
                if str(f1) not in self.finalstate or str(f2) not in self.finalstate:
                    continue
                self.addCut2GeneratorDatacard(f" all {Min} < {name} <= {Max} [{f1},{f2}] \n")

    def add_one_ParticleSelector(self, sel, name, unit=""):
        Min, Max = sel.get_MinMax(unit)
        f1 = sel.get_Flavours()
        for f in f1:
            f = self.pdg_to_whizard(f)
            self.addCut2GeneratorDatacard(f" all {Min} < {name} <= {Max} [{f}] \n")

    def addCut2GeneratorDatacard(self,cut):
        # the keyword for cuts: add once
        if self.CutKeyWdPresent is False:
            self.add2GeneratorDatacard("cuts = ")
            self.CutKeyWdPresent = True
        # the actual cuts
        if self.aCutIsPresent is False:
            self.add2GeneratorDatacard(f"{cut}")
            self.aCutIsPresent = True
        else:
            self.add2GeneratorDatacard(f" and {cut}")

    def write_integrate(self):
        for p in self.procs:
            self.add2GeneratorDatacard(f"integrate ({p})\n")
        self.add2GeneratorDatacard("simulate (proc) { iterations = 5:5000}\n")

    def fill_datacard(self):
        self.write_process()
        self.add2GeneratorDatacard("compile\n")
        self.write_integrate()

    def fill_key4hepScript(self):
        key4hepRun = ""
        # temporary fix for circe until we know where the files are stored in KEY4HEP
        if self.procinfo.get("beamstrahlung") is not None:
            accel = self.procinfo.get("beamstrahlung").upper()
            key4hepRun += f"wget https://whizard.hepforge.org/circe_files/{accel}/{self.procinfo.get_BeamstrahlungFile()}\n"
        # back to normal
        key4hepRun += self.executable + " " + self.GeneratorDatacardName + "\n"
        key4hepRun += "$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i {0} -o edm4hep proc.hepmc {1}.edm4hep\n".format(
            self.procinfo.get("output_format"), self.GeneratorDatacardBase
        )
        self.add2Key4hepScript(key4hepRun)

    def getModelName(self, model):
        modelDict = { 'sm' : 'SM_CKM'}
        if model.lower() not in modelDict.keys():
            print(f"Warning::Whizard: model {model} has no translation in Whizard Model Dictionary, using {model}")
            return model
        return modelDict[model.lower()]

    def getParameterLabel(self, param):
        parameterDict = { 'GFermi' : 'GF', 'alphaSMZ' : 'alphas',
                          'MZ' : 'mass', 'WZ' : 'width', 'MW' : 'mass', 'WW' : 'width',
                          'MB' : 'mass', 'MT' : 'mass', 'WT' : 'width', 'MH': 'mass', 'WH' : 'width'}
        # alphas could be SigmaProcess:alphaSvalue
        if param not in parameterDict.keys():
            print(f"Warning::Whizard: parameter {param} has no translation in Whizard Parameter Dictionary")
            return ""
        return parameterDict[param]

    def getParameterOperator(self, name):
        return f"{name}"

    def getGeneratorCommand(self,key,value):
        return f"{key} = {value}"

    def getParticleProperty(self, d):
        name = None
        if d == "mass":
            name = "MASS"
        if d == "width":
            name = "WIDTH"
        return name

    def getParticleOperator(self, pdg, prop):
        pname = self.whizard_MW_name(int(pdg))
        if prop == "MASS":
            return f"m{pname}"
        elif prop == "WIDTH":
            return f"w{pname}"


    def particle_to_whizard(self, particle):
        return particle.get("pdg_code")

    def pdg_to_whizard(self, pdg):
        apdg = abs(pdg)
        if type(pdg) is int:
            if 11 <= apdg <= 16:
                lepton_type = "e" if pdg % 2 == 1 else "n"
                flavor = (apdg - 11) // 2 + 1
                if pdg < 0:
                    lepton_type = lepton_type.capitalize()
                return f"{lepton_type}{flavor}"
            elif apdg > 20:
                particle_mapping = {22: "gamma", 23: "Z", 25: "H", 24: "Wp", -24: "Wm"}
                return particle_mapping.get(pdg, f"Cant find whizard id for pdg {pdg}")
            elif apdg <= 6:
                return self.whizard_quarks(pdg)
            else:
                return f"Cant find whizard id for pdg {pdg}"

    def whizard_quarks(self, pdg):
        quark_mapping = {1: "d", 2: "u", 3: "s", 4: "c", 5: "b", 6: "t"}
        q = quark_mapping.get(abs(pdg), "")
        return q.capitalize() if pdg > 0 else q

    def whizard_MW_name(self, pdg):
        if abs(pdg) <= 2:
            raise (ValueError, "Whizard does not support light quark masses or widths")
        if (abs(pdg) >= 12 and abs(pdg) <= 16) and pdg % 2 == 0:
            raise (ValueError, "Whizard does not support neutrino masses or widths")
        if abs(pdg) == 6:
            return "top"
        elif abs(pdg) == 15:
            return "tau"
        elif abs(pdg) == 24:
            return "W"
        else:
            return self.pdg_to_whizard(pdg)
