import abc
import importlib
import os, stat
import math
import ReleaseSpecs
import Parameters as ParameterModule
from Parameters import Parameter as ParameterClass
from Particles import Particle as ParticleClass
from Selectors import SelectorKeys

class GeneratorBase(abc.ABC):
    """GeneratorBase class"""

    def __init__(self, procinfo, settings, name, inputFileExtension):

        # general settings of the class
        self.procinfo = procinfo
        self.settings = settings
        self.name = name
        self.procDBName = f"{name}ProcDB"
        self.inputFileExtension    = inputFileExtension

        # set the Selectors Dictionary
        self.selectorsDict = dict()
        self.setSelectorsDict()
        self.validateSelectorsDict()

        # set the default model parameters:
        self.setDefaultModelParameters()
        # set the Generator specific parameters
        self.setModelParameters()
        # check consistency: note that the ParameterSets have been defined, check with the particle masses
        self.checkModelParameters()

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

        # four types of global variables for the file content
        self.__datacardContent = ""
        self.__key4hepContent  = ""
        self.__analysisContent = ""
        self.__optfileContent  = ""

        # optional file configuration
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
            #print(f"{self.procDBName} python module not found for {self.procinfo.get('_proclabel')}, no standard settings available")
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

        self.procDBparameters  = dict()
        self.procDBparticles  = dict()
        if self.settings.get("usedefaults", True):
            self.procDB.execute()
            self.procDBparameters  = self.procDB.getDictParameters()
            self.procDBparticles   = self.procDB.getDictParticles()

    def getModel(self):
        theModel = ""
        try:
            theModel = self.getModelName(self.gen_settings['model'])
        except:
            theModel = self.getModelName(self.procinfo.get('model'))
        return theModel

    def setSelectorsDict(self):
        raise NotImplementedError("setSelectorsDict")

    def validateSelectorsDict(self):
        # get the allowed keys
        keylistNominal = SelectorKeys().get_ParticleKeys()
        # check that every Generator key is in the predefined list
        for key in self.selectorsDict:
            if key not in keylistNominal:
                raise ValueError(f"{self.name} {key} not found in SelectorKeys list")

    def writeAllSelectors(self):
        selectors = getattr(self.settings, "selectors")
        try:
            procselectors = getattr(self.settings, "procselectors")
            for proc, sel in procselectors.items():
                if proc != self.procinfo.get("procname"):
                    continue
                for key, value in sel.items():
                    if value.process == self.procinfo.get("procname"):
                        self.writeSelector(value)
        except Exception as e:
            print(f"Failed to pass process specific cuts in {self.name}")
            print(e)
            pass
        for key, value in selectors.items():
            self.writeSelector(value)

    def writeSelector(self, select):
        # get the native key for the selector
        try:
            key = self.selectorsDict[select.name.lower()]
        except:
            print(f"{key} cannot be translated into a {self.name} selector")
            print(f"Ignoring the selector")
            return

        # add the selector implementation
        if select.NParticle == 1:
            self.add1ParticleSelector2Card(select, key)
        elif select.NParticle == 2:
            self.add2ParticleSelector2Card(select, key)
        else:
            print(f"{key} is a {select.NParticle} Particle selector, not implemented in {self.name}")

    def add1ParticleSelector2Card(self, sel, name):
        raise NotImplementedError(f"add1ParticleSelector not implemented in {self.name}")

    def add2ParticleSelector2Card(self, sel, name):
        raise NotImplementedError(f"add2ParticleSelector not implemented in {self.name}")

    def getModelName(self):
        raise NotImplementedError(f"getModelName not implemented in {self.name}")

    def setDefaultModelParameters(self):
        self.ModelInputParams = []
        self.addModelParameter('alphaSMZ')
        self.addModelParticleProperty(pdg_code=23, property_type='mass')
        self.addModelParticleProperty(pdg_code=6, property_type='mass')
        self.addModelParticleProperty(pdg_code=6, property_type='width')
        self.addModelParticleProperty(pdg_code=25, property_type='mass')
        self.addModelParticleProperty(pdg_code=25, property_type='width')

    def setModelParameters(self):
        raise NotImplementedError("setModelParameters")

    def checkModelParameters(self):
        # check alphaEM from MZ, MW and GFermi
        mW        = ParameterClass.get_info("MW").value
        mZ        = ParameterClass.get_info("MZ").value
        Gf        = ParameterClass.get_info("GFermi").value
        alphaEMLO = ParameterClass.get_info("alphaEMLO").value
        alphaEMLOPred = math.sqrt(2.)/math.pi*Gf*mW**2*(1.-mW**2/mZ**2)
        if not self.isCompatible(alphaEMLO, alphaEMLOPred):
            print(f"WARNING: alphaEMLO and GF, MW, MZ not compatible")
            print(f" Input: {alphaEMLO} Predicted: {alphaEMLOPred}")
        # check alphaEMLOM1 from alphaEMLO
        alphaEMLOM1 = ParameterClass.get_info("alphaEMLOM1").value
        alphaEMLOM1Pred = 1./alphaEMLO
        if not self.isCompatible(alphaEMLOM1, alphaEMLOM1Pred):
            print(f"WARNING: alphaEMLO and alphaEMLOM1 not compatible")
            print(f" Input: {alphaEMLOM1} Predicted: {alphaEMLOM1Pred}")
        # check sin2theta
        sin2thetaLO = ParameterClass.get_info("sin2thetaLO").value
        sin2thetaLOPred = 1.- mW**2 / mZ**2
        if not self.isCompatible(sin2thetaLO, sin2thetaLOPred):
            print(f"WARNING: sin2thetaLO not compatible with MW, MZ")
            print(f" Input: {sin2thetaLO} Predicted: {sin2thetaLOPred}")
        # check VEV
        vev = ParameterClass.get_info("VEV").value
        e2        = 4. *math.pi * alphaEMLO;
        g1sq      = e2/(1.-sin2thetaLO);
        g2sq      = e2/sin2thetaLO;
        vevLOPred = 2.* mZ/math.sqrt(g1sq+g2sq)
        if not self.isCompatible(vev, vevLOPred):
            print(f"WARNING: vev not compatible with sin2thetaLO")
            print(f" Input: {vev} Predicted: {vevLOPred}")

    def isCompatible(self, target, prediction):
        # maximum relative deviation
        maxRelDiff = 0.001
        # do the safe math
        relDelta = 1.
        # if the target is zero, then take the absolute deviation, if not the relative deviation
        if target > 0.:
            relDelta = abs(target - prediction ) / target
        else:
            relDelta = abs(target - prediction )
        # return compatibility or not
        if relDelta > maxRelDiff:
            return False
        return True

    def addModelParameter(self, item):
        if not self.hasModelParameter(item):
            self.ModelInputParams.append({'type' : 'Parameter', 'name' : item})

    def removeModelParameter(self, item):
        if self.hasModelParameter(item):
            self.ModelInputParams.remove({'type' : 'Parameter', 'name' : item})

    def hasModelParameter(self, item):
        if item in self.getModelParameterList():
            return True
        return False

    def getModelParameterList(self):
        paramList = []
        for item in self.ModelInputParams:
            if item['type'] == 'Parameter':
                paramList.append(item['name'])
        return paramList

    def addModelParticleProperty(self, pdg_code, property_type):
        if not self.hasModelParticleProperty(pdg_code, property_type):
            self.ModelInputParams.append({'type' : 'Particle', 'pdg' : pdg_code, 'prop' : property_type})

    def removeModelParticleProperty(self, pdg_code, property_type):
        if self.hasModelParticleProperty(pdg_code, property_type):
            self.ModelInputParams.remove({'type' : 'Particle', 'pdg' : pdg_code, 'prop' : property_type})

    def hasModelParticleProperty(self, pdg_code, property_type):
        if [pdg_code, property_type] in self.getModelParticlePropertyList():
            return True
        return False

    def getModelParticlePropertyList(self):
        particleList = []
        for item in self.ModelInputParams:
            if item['type'] == 'Particle':
                particleList.append([item['pdg'], item['prop']])
        return particleList

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

    def getGeneratorCommand(self,key,value):
        raise NotImplementedError("getGeneratorCommand")

    def addOption2GeneratorDatacard(self,key,value,replace=True):
        # check if the key is already defined in the datacard, then we take the last one (TBC):
        if replace is True:
            if key in self.__datacardContent:
                self.removeOptionGeneratorDatacard(key)
        # format the line through in the generator specific format
        if value is None:
            line = self.getGeneratorCommand(key,"")
        else:
            line = self.getGeneratorCommand(key,value)
        # add the linebreak
        line += "\n"
        # push to the datacard
        self.add2GeneratorDatacard(line)

    def replaceOptionInGeneratorDatacard(self,key,value):
        # check if the key is already defined in the datacard:
        if key in self.__datacardContent:
            if not isinstance(value, str):
                value = str(value)
            self.__datacardContent = self.__datacardContent.replace(key,value)
        else:
            print(f"Warning: {key} not set as defaults in {self.name}. Ignoring")

    def removeOptionGeneratorDatacard(self, opt):
        lines = self.__datacardContent.split("\n")
        filter_lines = [line for line in lines if opt not in line]
        self.__datacardContent = "\n".join(filter_lines)

    def prepareParameters(self):
        # 2 sources: global and procDB
        # hierarchy: global superseeds procDB
        # extract the Parameters:
        paramList = self.getModelParameterList()
        for param in paramList:
            # make sure that the parameters are in the global scope:
            if param in ParameterModule.ParametersList:
                if not ParameterClass.get_info(param).isParticleProperty:
                    globalParam = ParameterClass.get_info(param)
                    key         = self.getParameterLabel(param)
                    op_name     = self.getParameterOperator(key)
                    # write to datacard
                    self.addOption2GeneratorDatacard(op_name, globalParam.value)
                    # now check and remove operators in procDB if present:
                    if op_name in self.procDBparameters:
                        self.procDB.removeOption(op_name)
            else:
                print(f"Warning::GeneratorBase::prepareParameters: {param} not found")

    def getParameterLabel(self, param):
        raise NotImplementedError("getParameterLabel")

    def getParameterOperator(self, name):
        raise NotImplementedError("getParameterOperator")

    def prepareParticles(self,add2Datacard=True, writeParticleHeader=False):
        # three sources for the particles: YAML input, global and ProcDB
        # hierarchy: YAML superseeds global superseeds ProcDB
        # create a local dictionary then deal with the writing:
        particleCollection = dict()
        # load the procDB first
        for pdg in self.procDB.getDictParticles():
            # create an empty entry
            particleCollection[pdg] = dict()
            particle =  self.procDB.getDictParticles()[pdg]
            for prop in particle.keys():
                particleCollection[pdg].update({prop.lower(): particle[prop]})
                #particleCollection[pdg].update(particle[prop.lower()])

        # now we overwrite with global
        particleParameterList = self.getModelParticlePropertyList()
        for item in particleParameterList:
            pdg      = item[0]
            prop     = item[1]
            value    = 0
            particle = ParticleClass.get_info(pdg)
            if prop == "mass":
                value = particle.mass
            elif prop == "width":
                value = particle.width
            # need to convert to string for the keys
            pdgstr = str(pdg)
            # add/overwrite
            try:
                particle = particleCollection[pdgstr]
                particle[prop] = value
            except:
                particleCollection[pdgstr] = { prop : value }

        # now as last step we overwrite with the yaml if present:
        # retrieve the particles from the input
        for yamlParticle in self.procinfo.get_inputParticlesList():
            # loop over all attributes
            for attr in dir(yamlParticle):
                # make sure it's not a special attribute
                if not callable(getattr(yamlParticle, attr)) and not attr.startswith("__"):
                    # now we know it's a field name allowed by the generator:
                    if self.getParticleProperty(attr) is not None:
                        value  = getattr(yamlParticle, attr)
                        pdgstr = str(getattr(yamlParticle, 'pdg_code'))
                        # add/overwrite
                        try:
                            particle = particleCollection[pdgstr]
                            particle[attr] = value
                        except:
                            particleCollection[pdgstr] = { attr : value }

        # the list is complete, so we can loop over it to add it to the datacard
        for pdg in particleCollection.keys():
            particle = particleCollection[pdg]
            if writeParticleHeader is True and add2Datacard is True:
                self.addOption2GeneratorDatacard(self.getParticleOperator(pdg,None), None,replace=False)
            for attr in particle:
                value = particle[attr]
                prop  = self.getParticleProperty(attr)
                # writing out
                if prop is not None:
                    command = self.getParticleOperator(pdg,prop)
                    if add2Datacard is True:
                        self.addOption2GeneratorDatacard(command, value,replace=False)
                    else:
                        self.replaceOptionInGeneratorDatacard(command,value)

    def getParticleProperty(self, attr):
        raise NotImplementedError("getParticleProperty")

    def getParticleOperator(self, pdg, prop):
        raise NotImplementedError("getParticleOperator")

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

    def readTemplateFile(self):
        # Load default settigns
        try:
            with open(self.getTemplateFile(), "r") as file:
                return file.read()
        except FileNotFoundError as e:
            print("Cannot configure KKMC: Template file not found with error:\n"+str(e))
        return ""

    def getTemplateFile(self):
        return f"{os.path.dirname(__file__)}/{self.name}.template"

    def prepareKey4hepScript(self):
        # set up for key4hep run of event generation
        key4hep_config = "#!/usr/bin/env bash\n"
        key4hep_config += 'if [ -z "${KEY4HEP_STACK}" ]; then\n'
        # add the server extension for nightlies
        nightlies =""
        if ReleaseSpecs.key4hepUseNightlies.value:
            nightlies = "-nightlies"
        # add the explicite release date if requested
        releaseDate = ""
        if ReleaseSpecs.key4hepReleaseDate.value is not None:
            releaseDate = f" -r {ReleaseSpecs.key4hepReleaseDate.value}"
        # now we can configure the stuff correctly
        key4hep_config += (
            f"    source /cvmfs/sw{nightlies}.hsf.org/key4hep/setup.sh{releaseDate}\n"
        )
        key4hep_config += "fi\n\n"
        # store it
        self.add2Key4hepScript(key4hep_config)

    def prepareAnalysisContent(self):
        # analysis is conditioned on the output format
        outformat = self.settings.get_output_format()
        # write the EDM4HEP analysis part based on the final state
        analysis = "\n"
        if outformat == "edm4hep" and self.settings.key4HEPAnalysisON():
            analysis += f"key4HEPAnalysis -i {self.GeneratorDatacardBase}.edm4hep -o {self.GeneratorDatacardBase}.root -p "

            for pdg in self.procinfo.get_finalstate_pdgList():
                analysis += f"{pdg},"
            analysis = analysis.rstrip(",")
            analysis +="\n"

        # write the RIVET analysis
        if (outformat == "edm4hep" or outformat == "hepmc3") and self.settings.rivetON():
            yodaout = self.settings.yodaoutput + f"/{self.procinfo.get('procname')}.yoda"
            analysis += f"rivet"
            for ana in self.settings.analysisname:
                analysis += f" -a {ana}"
            analysis+=f" -o {yodaout} {self.procinfo.get('procname')}.{self.procinfo.get_output_format()}\n"

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

