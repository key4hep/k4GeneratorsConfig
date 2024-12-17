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
                generatorClass = getattr(generator,generatorName)
                # execute the object
                generatorObj = generatorClass(self.proc_info, self.settings)
                #writing file
                generatorObj.write_file()
                #writing key4hep file 
                generatorObj.write_key4hepfile()

            except ModuleNotFoundError:
                print(f"{generatorName} python module not found for {self.proc_info.get('_proclabel')}")
            except AttributeError:
                print(f"{generatorName} class could not be loaded with getattr for {self.proc_info.get('_proclabel')}")
            except:
                # all that remains is an excption from the execution of the modules
                print(f"Execution of {generatorName} for {self.proc_info.get('_proclabel')} resulted in an exception, check the module for problems with loading doownstream modules like the corresponding ProcDB etc")
                print("Datacard files and execution scripts not written for this generator")
                raise
