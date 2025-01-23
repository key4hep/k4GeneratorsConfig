import yaml
import os
import Selectors
import Parameters as ParameterModule
from Parameters import Parameter as ParameterClass

class Input:
    """Class for loading YAML files"""

    def __init__(self, file, sqrts):
        self.file = file
        self.settings = None
        self.anatool = None
        if not os.path.isfile(file):
            raise FileNotFoundError(file)
        else:
            self.load_file()

        for key, value in self.settings.items():
            if key.lower() == "events":
                try:
                    if "k" in value:
                        nvts = int(value.split("k")[0]) * 1e3
                        setattr(self, "events", nvts)
                    elif "m" in value:
                        nvts = int(value.split("m")[0]) * 1e6
                        setattr(self, "events", nvts)
                except:
                    setattr(self, "events", value)
            else:
                setattr(self, key.lower(), value)
        self.LoadCuts(sqrts)
        self.CheckDefaults()
        self.LoadAnalysis()

    def load_file(self):
        with open(self.file, "r") as file:
            self.settings = yaml.safe_load(file)
        self.settings = {k.lower(): v for k, v in self.settings.items()}

    def is_set(self, key):
        return hasattr(self, key)

    def get(self, key, default=None):
        try:
            return getattr(self, key)
        except:
            return default

    def get_block(self, key):
        try:
            return self.settings[key]
        except:
            return None

    def get_subblock(self, k1, k2):
        try:
            return self.settings[k1][k2]
        except:
            return None

    def gens(self):
        if not self.is_set("generators"):
            raise ValueError("No Generators set!")
        return getattr(self, "generators")

    def get_processes(self, sqrtsOverride=0):
        processes = getattr(self, "processes")
        if not processes:
            raise ValueError("No processes defined!")
        # Set all keys to be lower case
        for proc, value in processes.items():
            processes[proc] = {k.lower(): v for k, v in value.items()}
        # overwrite now sqrts with new value
        # now calculate the process extension if necessary
        if sqrtsOverride != 0:
            procExt = "_" + str(sqrtsOverride)
            processes = {proc + procExt: value for proc, value in processes.items()}
            for proc, values in processes.items():
                values["sqrts"] = sqrtsOverride

        return processes

    def get_output_format(self):
        outformat = ""
        # check for presence, if not: hepmc3
        try:
            outformat = self.settings["outputformat"]
        except:
            return "hepmc3"

        # check that only supported formats are requested
        if outformat != "hepmc2" and outformat != "hepmc3":
            print("OutputFormat " + outformat + " not supported using hepmc3")
            return "hepmc3"

        return outformat

    def get_Beamstrahlung(self):
        return self.get("beamstrahlung", None)

    def get_PythiaTune(self):
        return self.settings.get("pythiatune", None)

    def get_ElectronPolarisation(self):
        return self.settings.get("electronpolarisation", 0)

    def get_PositronPolarisation(self):
        return self.settings.get("positronpolarisation", 0)

    def get_PolDensity(self):
        return self.settings.get("poldensity", [1, -1])

    def get_sqrt_s(self):
        return self.get("sqrts", None)

    def get_particle_data(self):
        return self.get("particledata", None)

    def get_model(self):
        return self.get("model", "SM")

    def get_event_number(self):
        return self.get("events", 0)

    def get_isr_mode(self):
        return self.get("isrmode", 0)

    def get_ew_mode(self):
        return self.get("ewmode", 0)

    def get_weighted_mode(self):
        return self.get("eventmode", "unweighted")

    def set(self,key,value):
        setattr(self,key,value)

    def CheckDefaults(self):
        defaultName = ["initial", "isrmode", "beamstrahlung", "decay", "nlo"]
        defaultValue = [[11, -11], None, None, None, "lo"]
        for name, value in zip(defaultName, defaultValue):
            if not self.is_set(name):
                setattr(self, name, value)

    def LoadCuts(self,sqrtsOverride):
        # if self.get_block("selectors"):
        self.selectors = {}
        self.procselectors = {}
        pselectors = {}
        try:
            for proc in self.settings["selectors"]["Process"]:
                for key, sel in self.settings["selectors"]["Process"][proc].items():
                    # if sqrts >0, we have to extend the process ID with _sqrts so that the cuts are applied for all
                    if sqrtsOverride > 0. :
                        proc = proc+"_"+str(sqrtsOverride)
                    pselectors[proc + key] = Selectors.Selectors(proc, key, sel)
                self.procselectors[proc] = pselectors
        except Exception as e:
            print("Failed to find process specific cuts. Using global.")
            print(e)
            pass
        if self.get_block("selectors"):
            for name in self.get_block("selectors"):
                if name.lower() == "process":
                    continue
                self.selectors[name.lower()] = Selectors.Selectors(
                    name.lower(), self.settings["selectors"][name]
                )

    def LoadAnalysis(self):
        self.anasettings = self.get_block("analysis")
        if self.anasettings is not None:
            self.anasettings = {k.lower(): v for k, v in self.anasettings.items()}
            self.anatool = self.anasettings["tool"]
            self.anatool = self.anatool.lower()
            if self.anatool=="rivet":
                # check for rivet path
                if "RIVET_ANALYSIS_PATH" in os.environ:
                    self.rivetpath = os.environ["RIVET_ANALYSIS_PATH"]
                    if "rivetpath" in self.settings:
                        self.rivetpath = self.anasettings["rivetpath"]
                else:
                    try:
                        self.rivetpath = self.anasettings["rivetpath"]
                    except:
                        print("Rivet Analysis path has not been found")
                        self.anatool=None
                # Set the analysis name
                try:
                    self.analysisname = self.anasettings["rivetanalysis"]
                except:
                    print("No rivet analysis specified. Using MC_XS instead.")
                    print("Set an analysis with Analysis: RivetAnalysis: Name")
                    self.analysisname = ["MC_XS"]
                # Set yoda info
                try:
                    self.yodaoutput = self.anasettings["yodaoutdir"]
                except:
                    self.yodaoutput = os.getcwd()+"/yodafiles"
                    if not os.path.isdir(self.yodaoutput):
                        os.mkdir(self.yodaoutput)

    def IsRivet(self):
        return self.anatool=="rivet"

class ECMSInput:
    """Class for loading YAML files with center of mass energies"""

    def __init__(self, file):
        self.file = file
        if not os.path.isfile(self.file):
            raise FileNotFoundError(self.file)
        else:
            self.load_file()

    def load_file(self):
        with open(self.file, "r") as file:
            self.settings = yaml.safe_load(file)
        self.settings = {k.lower(): v for k, v in self.settings.items()}

    def energies(self):
        ecmsList = []
        for key, value in self.settings.items():
            ecmsList.extend(value)
        return ecmsList

class ParameterSets:
    """Class for loading YAML files with the parameter settings"""

    def __init__(self, file, tag):
        self.file = file
        if not os.path.isfile(self.file):
            raise FileNotFoundError(self.file)
        else:
            self.load_file(tag)

    def load_file(self, tag):
        with open(self.file, "r") as file:
            settings = yaml.safe_load(file)

        # now we can safe the requested tag to the settings:
        settings = settings.get(tag, None)
        if settings is None:
            raise FileNotFoundError(f"Error: tag {tag} not found in {self.file}")
        # check the validity of the keys and store in the global dictionary
        for key in settings.keys():
            if key not in ParameterModule.ParametersList:
                print(f"Warning! parameterTag: {tag} unknown key: {key} ignored")
            else:
                try:
                    param = ParameterClass.get_info(key)
                    param.value = settings[key]
                except ValueError as e:
                    print("Error setting ParameterSet parameter: parameter not coded in Parameters.py")
                    print(e)
                    exit()

