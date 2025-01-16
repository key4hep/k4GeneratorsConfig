import abc
import importlib
import os, stat

class GeneratorBase(abc.ABC):
    """GeneratorBase class"""

    def __init__(self, procinfo, settings, name, inputFileExtension):

        # general settings of the class
        self.procinfo = procinfo
        self.settings = settings
        self.name = name
        self.procDBName = f"{name}ProcDB"
        self.inputFileExtension    = inputFileExtension

        # define the output directory as function of the OutDir spec + generator name + process name
        self.outdir = (
            f"{procinfo.get('OutDir')}/{self.name}/{self.procinfo.get('procname')}"
        )

        # configure the filenames
        self.GeneratorDatacardBase = f"{self.procinfo.get('procname')}"
        self.key4hepScript = f"{self.outdir}/Run_{self.procinfo.get('procname')}"

        # add ISR and BST if requested
        if self.procinfo.get("isrmode"):
            self.GeneratorDatacardBase += "_ISR"
            self.key4hepScript += "_ISR"

            if self.procinfo.get("beamstrahlung") is not None:
                self.GeneratorDatacardBase += (
                    "_BST" + self.procinfo.beamstrahlung.lower()
                )
                self.key4hepScript += "_BST" + self.procinfo.beamstrahlung.lower()

        # take care of the extensions of the filenames
        self.GeneratorDatacardName = (
            self.GeneratorDatacardBase + "." + self.inputFileExtension
        )
        self.key4hepScript += ".sh"

        # composition of file+directory
        self.GeneratorDatacard = f"{self.outdir}/{self.GeneratorDatacardName}"

        # three types of global variables for the file content
        self.__datacardContent = ""
        self.__key4hepContent  = ""
        self.__analysisContent = "" 
        self.__optfileContent  = "" 

        self.__optionalFileExtension = ""
        self.__optionalFileName      = ""
        self.__optionalFile          = ""
        self.__optionalFileUsed      = False

        # the KEY4HEP environment setup is independent of the generator, so we can prepare it at the initialization stage:
        self.prepareKey4hepScript()
        
        # the analysis depends only on the process, not on the generator, so we can prepare it at the initialization stage:
        self.prepareAnalysisContent()

        # the generator settings are stored in a public member:
        self.gen_settings = settings.get_block(self.name.lower())
        if self.gen_settings is not None:
            self.gen_settings = {k.lower(): v for k, v in self.gen_settings.items()}

        # the generator ProcDB settings are stored in a public member:
        try:
            generatorProcDB      = importlib.import_module(f"Generators.{self.procDBName}")
            # get the ClassObject
            generatorProcDBClass = getattr(generatorProcDB,self.procDBName)
            # execute the object
            self.procDB          = generatorProcDBClass(self.procinfo)
        except ModuleNotFoundError:
            print(f"{self.procDBName} python module not found for {self.procinfo.get('_proclabel')}, no standard settings available")
            # load the baseclass in this case to ensure execution
            baseClass = "ProcDBBase"
            generatorProcDB      = importlib.import_module(f"Generators.{baseClass}")
            # get the ClassObject
            generatorProcDBClass = getattr(generatorProcDB,baseClass)
            # execute the object
            self.procDB          = generatorProcDBClass(self.procinfo)
        except AttributeError:
            print(f"{self.procDBName} class could not be loaded with getattr for {self.procinfo.get('_proclabel')} or class initialization did not work")
        except:
            # all that remains is an excption from the execution of the modules
            print(f"Execution of {self.procDBName} for {self.procinfo.get('_proclabel')} resulted in an exception")
            print("Datacard files and execution scripts not written for this generator")
            raise
        
        self.procDB_settings = dict()
        if self.settings.get("usedefaults", True):
            self.procDB.write_DBInfo()
            self.procDB_settings = self.procDB.getDict()
        
    def execute(self):
        raise NotImplementedError("execute")

    def add2GeneratorDatacard(self,content):
        # data encapsulation: add to the content in the base class
        self.__datacardContent += content
       
    def getGeneratorDatacard(self):
        # return content
        return self.__datacardContent
       
    def resetGeneratorDatacard(self):
        # data encapsulation: reset the datacard content to ""
        self.__datacardContent = ""
       
    def formatLine(self,key,value):
        raise NotImplementedError("formatLine")

    def addOption2GeneratorDatacard(self,key,value):
        # check if the key is already defined in the datacard, then we take the last one (TBC):
        if key in self.__datacardContent:
            self.removeOptionGeneratorDatacard(key)
        # format the line through in the generator specific format
        if value is None:
            line = self.formatLine(key,"")
        else:
            line = self.formatLine(key,value)
        # add the linebreak
        line += "\n"
        # push to the datacard
        self.add2GeneratorDatacard(line)

    def removeOptionGeneratorDatacard(self, opt):
        lines = self.__datacardContent.split("\n")
        filter_lines = [line for line in lines if opt not in line]
        self.__datacardContent = "\n".join(filter_lines)

    def prepareParticles(self):
        # retrieve the particles from the input
        for part in self.procinfo.get_data_particles():
            # loop over all attributes
            for attr in dir(part):
                # make sure it's not a special attribute
                if not callable(getattr(part, attr)) and not attr.startswith("__"):
                    # now we know it's just a field name:
                    prop = self.is_particle_data(attr)
                    if prop is not None:
                        op_name = self.get_particle_operator(part,prop)
                        # remove from the Standard=ProcDB settings if necessary
                        if op_name in self.procDB_settings:
                            self.procDB.removeOption(op_name)
                        value = getattr(part, attr)
                        self.addOption2GeneratorDatacard(op_name, value)

    def is_particle_data(self, attr):
        raise NotImplementedError()

    def get_particle_operator(self, part, name):
        raise NotImplementedError()

    def add2Key4hepScript(self,content):
        # data encapsulation: add to the content in the base class
        self.__key4hepContent += content
        
    def getKey4hepScript(self):
        # return content
        return self.__key4hepContent
        
    def resetKey4hepScript(self):
        # data encapsulation: reset the  KEY4HEP script content to ""
        self.__key4hepContent = ""
        
    def add2Analysis(self,content):
        # data encapsulation: add to the content in the base class
        self.__analysisContent += content
        
    def getAnalysis(self):
        # return content
        return self.__analysisContent
        
    def resetAnalysis(self):
        # data encapsulation: reset analysis content to ""
        self.__analysisContent = ""
        
    def add2OptionalFile(self,content):
        # data encapsulation: add to the content in the base class
        if not self.__optionalFileUsed:
            self.__optionalFileUsed = True
        self.__optfileContent += content
       
    def getOptionalFileContent(self):
        # return content
        return self.__optfileContent
       
    def resetOptionalFile(self):
        # data encapsulation: reset the optionalFile content to ""
        self.__optfileContent = ""
       
    def setOptionalFileNameAndExtension(self,filename,extension):
        # data encapsulation: reset the optionalFile content to ""
        self.__optionalFileExtension = extension
        self.__optionalFileName      = f"{filename}.{self.__optionalFileExtension}"
        self.__optionalFile          = f"{self.outdir}/{filename}.{self.__optionalFileExtension}"
        if not self.__optionalFileUsed:
            self.__optionalFileUsed = True
       
    def getOptionalFileName(self):
        return self.__optionalFileName
       
    def prepareKey4hepScript(self):
        # set up for key4hep run of event generation
        key4hep_config = "#!/usr/bin/env bash\n"
        key4hep_config += 'if [ -z "${KEY4HEP_STACK}" ]; then\n'
        key4hep_config += (
            "    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh\n"
        )
        key4hep_config += "fi\n\n"
        # store it
        self.add2Key4hepScript(key4hep_config)

    def prepareAnalysisContent(self):
        # write the EDM4HEP analysis part based on the final state
        analysis = "\n"
        finalStateList = [int(pdg) for pdg in self.procinfo.get_final_pdg().split(" ")]
        if len(finalStateList) == 2:
            analysis += "$K4GenBuildDir/bin/analyze2f -a {0} -b {1} -i {2}.edm4hep -o {2}.root\n".format(
                finalStateList[0], finalStateList[1], self.GeneratorDatacardBase
            )

        # write the RIVET analysis
        if self.settings.IsRivet():
            yodaout = self.settings.yodaoutput + f"/{self.procinfo.get('procname')}.yoda"
            analysis += f"rivet" 
            for ana in self.settings.analysisname:
                analysis += f" -a {ana}"
            analysis+=f" -o {yodaout} {self.procinfo.get('procname')}.{self.procinfo.get('output_format')}\n"

        # add to the text to the data member
        self.add2Analysis(analysis)
    
    def finalize(self):
        # the content has been filled, now we write to disk
        self.writeGeneratorDatacard()
        self.writeKey4hepScript()
        self.writeOptionalFile()

    def writeGeneratorDatacard(self):
        with open(self.GeneratorDatacard, "w+") as file:
            file.write(self.__datacardContent)

    def writeKey4hepScript(self):
        # open the file for the evgen generation in EDM4HEP format
        with open(self.key4hepScript, "w+") as file:
            # set up KEY4HEP
            file.write(self.__key4hepContent)
            # set up Analysis
            file.write(self.__analysisContent)
        # make the script executable
        os.chmod(self.key4hepScript, os.stat(self.key4hepScript).st_mode | stat.S_IEXEC)

    def writeOptionalFile(self):
        if self.__optionalFileUsed:
            with open(self.__optionalFile, "w+") as file:
                file.write(self.__optfileContent)

