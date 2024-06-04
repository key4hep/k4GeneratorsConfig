from Particles import Particle
from CirceHelper import CirceHelper

class Process:
    """A standard Process"""

    _required_args = ['initial', 'final', 'sqrts', 'order', 'randomseed', 'decay', 'isrmode','beamstrahlung']

    def __init__(self, args, procname, params, **options):
        self._init = False
        self._parts = []
        self._dataparts = []
        self.generatorDBLabel = ""
        self.procname = procname

        for arg in self._required_args:
            setattr(self, arg, params.settings.get(arg))
        
        for setting in dir(params):
            if not setting.startswith("__"):
                setattr(self, setting, getattr(params, setting))

        for option, value in options.items():
            setattr(self, option, value)

        for key,value in args.items():
            setattr(self, key, value)

    def process_info(self):
        self._beam1 = Particle.get_info(self.initial[0])
        self._beam2 = Particle.get_info(self.initial[1])
        self._finfo = {}
        self._fpdg = []
        self._parts.extend([self._beam1, self._beam2])
        self._proclabel = "{} {} -> ".format(self._beam1.name, self._beam2.name)
        for p in self.final:
            self._finfo[p] = Particle.get_info(p)
            self._fpdg.append(str(p))
            self._proclabel += f"{self._finfo[p].name} "
            self._parts.append(self._finfo[p])
        # generate the label for the generatorDB 
        finalstate = [abs(part) for part in self.final]
        # sort ascending
        finalstate.sort()
        for pdg in finalstate:
            self.generatorDBLabel += f"_{str(abs(pdg))}"
        # remove leading _
        self.generatorDBLabel = self.generatorDBLabel[(self.generatorDBLabel.index("_")+1):] 

    def set_particle_data(self, pdata):
        if pdata is None or self._init:
            return
        for key, value in pdata.items():
            Particle.set_info(key, value)
            self._dataparts.append(Particle.get_info(key))
        self._init = True

    def get_beam_flavour(self, beam):
        if beam not in {1, 2}:
            raise ValueError("Beam should be 1 or 2 not {}".format(beam))
        return getattr(self, f"_beam{beam}").get("pdg_code")

    def get_initial_pdg(self):
        return "{} {}".format(self.get_beam_flavour(1), self.get_beam_flavour(2))

    def get_final_pdg(self):
        return " ".join(self._fpdg)

    def get_final_pdg_list(self):
        return list(self._finfo)

    def get(self, name):
        return getattr(self, name)

    def get_args(self):
        return self._required_args

    def get_particles(self):
        return self._parts

    def get_data_particles(self):
        return self._dataparts

    def get_qcd_order(self):
        return self.get("order")[1]

    def get_qed_order(self):
        return self.get("order")[0]

    def get_output_format(self):
        return self.output_format

    def get_PythiaTune(self):
        return self.PythiaTune

    def get_ElectronPolarisation(self):
        return self.ElectronPolarisation

    def get_PositronPolarisation(self):
        return self.PositronPolarisation

    def get_PolDensity(self):
        return self.PolDensity

    def get_rndmSeed(self):
        return self.get("randomseed")

    def get_BeamstrahlungFile(self):
        if self.get("beamstrahlung") is not None:
            circe = CirceHelper(self.beamstrahlung,self.sqrts) 
            return circe.getFile()

    def get_generatorDBLabel(self):
        return self.generatorDBLabel

    def print_info(self):
        out = f"Creating Runcards for {self._proclabel} at {self.sqrts} GeV"
        print(out)
        print("Particles are defined with the following parameters")
        for p in self._parts:
            p.print_info()


class ProcessParameters:


    def __init__(self, settings):
        self.settings = settings
        self.model = settings.get_model()
        self.events = settings.get_event_number()
        self.output_format        = settings.get_output_format()
        self.PythiaTune           = settings.get_PythiaTune()
        self.ElectronPolarisation = settings.get_ElectronPolarisation()
        self.PositronPolarisation = settings.get_PositronPolarisation()
        self.PolDensity = settings.get_PolDensity()
        self.eventmode = settings.get_weighted_mode()
        self.ewmode = settings.get_ew_mode()
