import importlib

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
                generator   = importlib.import_module(f"Generators.{generatorName}")
                # get the ClassObject
                if hasattr(generator,generatorName):
                    generatorClass = getattr(generator,generatorName)
                    # execute the object
                    try:
                        generatorObj = generatorClass(self.proc_info, self.settings)
                        #writing file
                        generatorObj.write_file()
                        #writing key4hep file 
                        generatorObj.write_key4hepfile()
                    except:
                        print(f"Requested Generator: {generatorName} object could not be executed, output files not written for {self.proc_info.get('_proclabel')}")
                else:
                    print(f"Requested Generator: {generatorName} class could not be loaded via getattr {self.proc_info.get('_proclabel')}")
            except:
                print(f"Requested Generator: {generatorName} could not be configured for {self.proc_info.get('_proclabel')}")
