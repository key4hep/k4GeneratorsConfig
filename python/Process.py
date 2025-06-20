from Particles import Particle
from Generators.CirceHelper import CirceHelper


class Process:
    """A standard Process"""

    _required_args = [
        "initial",
        "final",
        "sqrts",
        "order",
        "nlo",
        "randomseed",
        "decay",
        "isrmode",
        "beamstrahlung",
    ]

    def __init__(self, args, procname, params, particleData, **options):
        # list of particles filled from the input yaml file
        self._inputParticlesList = []
        if particleData is not None:
            for key, value in particleData.items():
                Particle.set_info(key, value)
                self._inputParticlesList.append(Particle.get_info(key))
        # all particles in process list
        self._particlesOfProcessList = []
        # label to be used in the generatorDB
        self.generatorDBLabel = ""
        self.procname = procname

        for arg in self._required_args:
            setattr(self, arg, params.settings.get(arg))
        for setting in dir(params):
            if not setting.startswith("__"):
                setattr(self, setting, getattr(params, setting))

        for option, value in options.items():
            setattr(self, option, value)

        for key, value in args.items():
            setattr(self, key, value)

    def prepareProcess(self):
        # beam particles
        self._beam1 = Particle.get_info(self.initial[0])
        self._beam2 = Particle.get_info(self.initial[1])
        # final state particle dictionary
        self._finalStateParticleDict = {}
        # final state particle list
        self._finalStatePDGList = []
        # add beam to all particles list
        self._particlesOfProcessList.extend([self._beam1, self._beam2])
        # full process label
        self._proclabel = "{} {} -> ".format(self._beam1.name, self._beam2.name)
        for p in self.final:
            self._finalStateParticleDict[p] = Particle.get_info(p)
            self._finalStatePDGList.append(str(p))
            self._proclabel += f"{self._finalStateParticleDict[p].name} "
            self._particlesOfProcessList.append(self._finalStateParticleDict[p])
        # generate the label for the generatorDB
        # first the initial state
        initialstate = [abs(self.initial[0]), abs(self.initial[1])]
        #sort ascending
        initialstate.sort()
        # add to label
        for pdg in initialstate:
            self.generatorDBLabel += f"_{str(abs(pdg))}"
        # remove leading "_"
        self.generatorDBLabel = self.generatorDBLabel[
            (self.generatorDBLabel.index("_") + 1) :
        ]
        # now the final state
        finalstate = [abs(part) for part in self.final]
        # sort ascending
        finalstate.sort()
        # add to label
        for pdg in finalstate:
            self.generatorDBLabel += f"_{str(abs(pdg))}"

    def get_beam_flavour(self, beam):
        if beam not in {1, 2}:
            raise ValueError("Beam should be 1 or 2 not {}".format(beam))
        return getattr(self, f"_beam{beam}").get("pdg_code")

    def get_initialstate_pdgString(self):
        return "{} {}".format(self.get_beam_flavour(1), self.get_beam_flavour(2))

    def get_finalstate_pdgString(self):
        return " ".join(self._finalStatePDGList)

    def get_finalstate_pdgList(self):
        return self._finalStatePDGList

    def get_finalstate_pdgDictList(self):
        return list(self._finalStateParticleDict)

    def get(self, name):
        try:
            return getattr(self, name)
        except:
            return None

    def get_args(self):
        return self._required_args

    def get_particlesOfProcessList(self):
        return self._particlesOfProcessList

    def get_inputParticlesList(self):
        return self._inputParticlesList

    def get_qcd_order(self):
        return self.get("order")[1]

    def get_qed_order(self):
        return self.get("order")[0]

    def get_nlo(self):
        return self.get("nlo")

    def get_output_format(self):
        return self.output_format

    def get_PythiaTune(self):
        return self.PythiaTune

    def get_PolarisationDensity(self):
        return self.PolarisationDensity

    def get_PolarisationFraction(self):
        return self.PolarisationFraction

    def get_rndmSeed(self):
        return self.get("randomseed")

    def get_BeamstrahlungFile(self):
        if self.get("beamstrahlung") is not None:
            circe = CirceHelper(self.beamstrahlung, self.sqrts)
            return circe.getFile()

    def get_generatorDBLabel(self):
        return self.generatorDBLabel

    def print_info(self):
        print(f"Creating Runcards for {self._proclabel} at {self.sqrts} GeV")
        print("Particles are defined with the following parameters")
        for part in self._particlesOfProcessList:
            part.print_info()


class ProcessParameters:
    def __init__(self, settings):
        self.settings      = settings
        self.model         = settings.get_model()
        self.events        = settings.get_event_number()
        self.output_format = settings.get_output_format()
        self.PythiaTune    = settings.get_PythiaTune()
        self.PolarisationDensity    = settings.get_PolarisationDensity()
        self.PolarisationFraction   = settings.get_PolarisationFraction()
        self.eventmode     = settings.get_weighted_mode()
        self.ewmode        = settings.get_ew_mode()
