import importlib

from . import Sherpa
from . import Whizard
from . import Madgraph
from . import Babayaga
from . import KKMC
from . import Pythia


class Generators:
    """Generator class"""

    def __init__(self, settings):
        self.settings = settings
        self.generator_list = settings.gens()

    def set_process_info(self, proc_info):
        self.proc_info = proc_info

    def initialize_generators(self):

        for generatorName in self.generator_list:
            # get the module
            try:
                generator   = importlib.import_module(generatorName)
                # get the ClassObject
                generatorClass = getattr(generator,generatorName)
                # execute the object
                generatorObj = generatorClass(self.proc_info, self.settings)
                #writing file
                generatorObj.write_file()
                #writing key4hep file 
                generatorObj.write_key4hepfile()
            except:
                print("Requested Generator: "+generatorName+" could not be configured for "+self.proc_info.get("_proclabel"))
