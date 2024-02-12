import yaml
import os

class Input:
    """Class for loading YAML files"""
    def __init__(self, file):
        self.file = file
        self.settings = None
        if not os.path.isfile(file):
            raise FileNotFoundError(file)
        else:
            self.load_file()

        for key,value in self.settings.items():
        	setattr(self, key, value)

    def load_file(self):
        with open(self.file, 'r') as file:
            self.settings = yaml.safe_load(file)

    def is_empty(self, key):
        return key not in self.settings

    def generators(self):
        if self.is_empty("Generators"):
            raise ValueError("No Generators set!")
        return self.settings["Generators"]

    def get_processes(self):
        processes = self.settings.get("Processes", [])
        if not processes:
            raise ValueError("No processes defined!")
        return processes

    def get_output_format(self):
        try:
            return self.settings["OutputFormat"]
        except:
            return "hepmc"

    def get_rndmSeed(self):
        try:
            return self.settings["RandomSeed"]
        except:
            return 4711

    def get_Beamstrahlung(self):
        try:
            return self.settings["Beamstrahlung"]
        except:
            return "ILC"

    def get_PythiaTune(self):
        try:
            return self.settings["PythiaTune"]
        except:
            return "None"

    def get_ElectronPolarisation(self):
        try:
            return self.settings["ElectronPolarisation"]
        except:
            return 0

    def get_PositronPolarisation(self):
        try:
            return self.settings["PositronPolarisation"]
        except:
            return 0

    def get_sqrt_s(self):
        return self.settings.get("SqrtS", None)

    def get_particle_data(self):
        return self.settings.get("ParticleData", None)

    def get_model(self):
        return self.settings.get("Model", "SM")

    def get_event_number(self):
        return self.settings.get("Events", 0)

    def get_isr_mode(self):
        return self.settings.get("ISRMode", 0)
