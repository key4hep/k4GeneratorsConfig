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

    def load_file(self):
        with open(self.file, 'r') as file:
            self.settings = yaml.safe_load(file)
        self.settings = {k.lower(): v for k, v in self.settings.items()}

    def is_set(self, key):
        return hasattr(self, key)
        
    def get(self, key, default=None):
        try:
            return getattr(self, key)
        except:
            return default

    def get_block(self,key):
        try:
            return self.settings[key]
        except:
            return None

    def gens(self):
        if not self.is_set("generators"):
            raise ValueError("No Generators set!")
        return getattr(self, "generators")

    def get_processes(self):
        processes = getattr(self,"processes")
        if not processes:
            raise ValueError("No processes defined!")
        # Set all keys to be lower case 
        for proc, value in processes.items():
            processes[proc] = {k.lower(): v for k, v in value.items()}
        return processes

    def get_output_format(self):
        try:
            return self.settings["ouputformat"]
        except:
            return "hepmc"

    def get_rndmSeed(self):
        try:
            return getattr(self,"randomseed")
        except:
            return 4711

    def get_sqrt_s(self):
        return self.get("sqrts", None)

    def get_particle_data(self):
        return self.get("particledata", None)

    def get_model(self):
        return self.get("model", "SM")

    def get_event_number(self):
        return self.get("events", 0)
        # nvts = self.get("events", 0)
        # if "k" in nvts:
        #     nvts = int(nvts.split("k")[0]) * 1e3
        #     setattr(self, "events", nvts)
        # elif "m" in nvts:
        #     nvts = int(nvts.split("m")[0]) * 1e6
        #     setattr(self, "events", nvts)
        # return nvts            



    def get_isr_mode(self):
        return self.get("isrmode", 0)
