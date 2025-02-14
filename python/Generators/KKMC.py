import os, sys
from .GeneratorBase import GeneratorBase
import Parameters as ParameterModule
from Parameters import Parameter as ParameterClass

class KKMC(GeneratorBase):
    """KKMC class"""

    def __init__(self, procinfo, settings):
        super().__init__(procinfo, settings, "KKMC", "dat")

        self.version = "x.y.z"
        self.executable = "KKMC-fcc.exe"

        self.add2GeneratorDatacard(self.readTemplateFile())

    def setModelParameters(self):
        # there are some parameters we cannot set
        self.removeModelParticleProperty(pdg_code=6, property_type='width')
        self.removeModelParticleProperty(pdg_code=25, property_type='mass')
        self.removeModelParticleProperty(pdg_code=25, property_type='width')
        # parameters to be set
        self.addModelParameter('GFermi')
        self.addModelParameter('alphaEMM1')
        # need to ensure MZ, Mtop are set:
        self.addModelParticleProperty(pdg_code=23, property_type='mass')
        self.addModelParticleProperty(pdg_code=23, property_type='width')
        self.addModelParticleProperty(pdg_code=6,  property_type='mass')

    def execute(self):
        # prepare the datacard
        self.fill_datacard()
        # prepare the key4hep script
        self.fill_key4hepScript()
        
    def fill_datacard(self):
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
        self.replaceOptionInGeneratorDatacard("_seed", self.procinfo.get_rndmSeed())
        self.replaceOptionInGeneratorDatacard("_energy", self.procinfo.get("sqrts"))
        self.replaceOptionInGeneratorDatacard("_besdelta", 0)
        # TODO add bes
        self.replaceOptionInGeneratorDatacard("_besmode", 0)
        self.replaceOptionInGeneratorDatacard("_ewmode", self.procinfo.get("ewmode"))
        self.replaceOptionInGeneratorDatacard("_isrmode", self.procinfo.get("isrmode"))
        self.replaceOptionInGeneratorDatacard("_fsrmode", self.settings.get("fsrmode", 0))
        self.replaceOptionInGeneratorDatacard("_FINALSTATES", f"  {self.finalstate}              1")

        # output format only hepm2 or hepmc3, the actual version is detected by the linked library, so strip the number
        if self.procinfo.eventmode == "unweighted":
            self.replaceOptionInGeneratorDatacard("_wgtmode", "0")
        else:
            self.replaceOptionInGeneratorDatacard("_wgtmode", "1")

        # now take care of the EW parameters
        for param in self.getModelParameterList():
            # make sure that the parameters are in the global scope:
            if param in ParameterModule.ParametersList:
                globalParam = ParameterClass.get_info(param)
                key         = self.getParameterLabel(param)
                self.replaceOptionInGeneratorDatacard(key, globalParam.value)
            else:
                raise RuntimeError(f"ERROR:{self.name}: {param} not found in global parameter list")
        # now take care of the particles
        self.prepareParticles(add2Datacard=False)

    def add_decay(self):
        print("DECAY specified, cannot be implmented in KKMC")

    def fill_key4hepScript(self):
        key4hepRun = ""
        key4hepRun += "KKMCee -c  {0} --nevts {3} -o {1}.{2}\n".format(
            self.GeneratorDatacardName,
            self.GeneratorDatacardBase,
            self.procinfo.get("output_format"),
            self.procinfo.get("events"),
        )
        key4hepRun += "$K4GenBuildDir/bin/convertHepMC2EDM4HEP -i {0} -o edm4hep {1}.{0} {1}.edm4hep\n".format(
            self.procinfo.get("output_format"), self.GeneratorDatacardBase
        )
        self.add2Key4hepScript(key4hepRun)

    def getParameterLabel(self, param):
        parameterDict = { 'GFermi' : '_GFermi', 'alphaSMZ' : '_alphaSMZ', 'alphaEMM1': '_alphaEMM1'}
        # alphas could be SigmaProcess:alphaSvalue 
        if param not in parameterDict.keys():
            print(f"Warning::KKMC: parameter {param} has no translation in KKMC Parameter Dictionary")
            return ""
        return parameterDict[param]

    def getParticleProperty(self, d):
        name = None
        if d == "mass":
            name = "MASS"
        if d == "width":
            name = "WIDTH"
        return name

    def getParticleOperator(self, pdg, prop):
        if prop == "MASS":
            return f"_mass{pdg}"
        elif prop == "WIDTH":
            return f"_width{pdg}"

    def pdg_to_KKMC(self, pdg):
        apdg = abs(400 + int(pdg))
        return f"{apdg}"
