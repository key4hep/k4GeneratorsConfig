from abc import ABC,abstractmethod
import os
import sys
import shutil
from pathlib import Path
import filecmp

from main import main

class CIUtilsBase(ABC):
    """Generator Generator Datacards"""
    def __init__(self, workDirectory, outputDirectory):

        # consistent processing of names
        self._workDir = os.path.dirname(os.path.realpath(__file__))+"/"+workDirectory
        if workDirectory.startswith("/"):
            self._workDir = args.workDir

        self.outDir = os.path.dirname(os.path.realpath(__file__))+"/"+outputDirectory
        if outputDirectory.startswith("/"):
            self.outdir = outputDirectory

        self._referenceDir = os.path.dirname(os.path.realpath(__file__))+"/../test/ref-results"


class createGeneratorDatacards(CIUtilsBase):
    """Generator Generator Datacards"""

    def __init__(self, yamlDirectory, yamlFile, workDirectory, outputDirectory):
        super().__init__(workDirectory, outputDirectory)

        # specific members for DC creation
        self._yamlDir = os.path.dirname(os.path.realpath(__file__))+"/"+yamlDirectory
        if yamlDirectory.startswith("/"):
            self._yamlDir = yamlDirectory

        self._yamlFiles = []

        # make the directory for the work
        self.makeDirectory(workDirectory)
        # make the output directory for the output
        self.makeDirectory(outputDirectory)

        # prepare yamls:
        self.prepareYamls(yamlFile);

        # prepare the Sqrts files:
        self.prepareECMS();

        # process all yamls:
        self.process();

    def makeDirectory(self, dirname):
        # Overwrite directory if it exists
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        else:
            shutil.rmtree(dirname)
            os.makedirs(dirname)

    def prepareYamls(self, yamlFile):
        # move the yamls to the work directory
        # the yaml file is not specified copy all yaml files to the work directory:
        if yamlFile == "None":
            self._yamlFiles = [filename for filename in os.listdir(self._yamlDir) if filename.endswith('.yaml')]
        else:
            self._yamlFiles =[self.yamlDir+"/"+yamlFile]

        # copy the yaml files
        for filename in self._yamlFiles:
            shutil.copy(os.path.join(self._yamlDir,filename),self._workDir)

    def prepareECMS(self):
        # move the ECMS files to the work directory
        ecmsFiles = [filename for filename in os.listdir(self._yamlDir) if filename.endswith('.dat') and filename.startswith('ecms')]

        # copy the yaml files
        for filename in ecmsFiles:
            shutil.copy(os.path.join(self._yamlDir,filename),self._workDir)

    def process(self):
        # go to the working directory
        os.chdir(self._workDir)
        # loop over all files
        for filename in self._yamlFiles:
            processName = Path(filename).stem
            ecmsName = "ecms"+processName+".dat"
            print("Processing : "+processName)
            if os.path.isfile(ecmsName):
                main([filename,'--ecmsFile',ecmsName])
            else:
                main([filename])

class checkGeneratorDatacards(CIUtilsBase):
    """Check Generator Datacards"""

    def __init__(self, generator, workDirectory, outputDirectory):
        super().__init__(workDirectory, outputDirectory)

        # specific stuff:
        self.generatorDir = self._workDir+"/Run-Cards"
        
        # retrieve all generators in the workdirector:
        generators = self.getGenerators(generator)

        # now compare to reference
        self.process(generators)

    def getGenerators(self, generator):
        if generator == "All":
            return os.listdir(self.generatorDir)
        else:
            return [generator]
        
    def getProcesses(self, generator):
        return os.listdir(self.generatorDir+"/"+generator)
        
    def getFileNames(self, directory):
        filenames = os.listdir(directory)
        filenames =[name for name in filenames if os.path.isfile(os.path.join(directory,name))]
        return filenames

    def process(self, generators):
        failure = False

        for generator in generators:
            processes = self.getProcesses(generator)

            for proc in processes:
                genProc = "/"+generator+"/"+proc
                newDir = self.generatorDir+genProc
                refDir = self._referenceDir+genProc
                fileNames = self.getFileNames(refDir)

                for name in fileNames:
                    newFile = newDir+"/"+name
                    refFile = refDir+"/"+name
                    message = "Generator "+generator+" Process "+proc+" File "+name
                    if filecmp.cmp(refFile,newFile, shallow=False):
                        print(message+" identical")
                    else:
                        print(message+" differ")
                        failure = True
        if failure:
            sys.exit("Failed comparison")
        

class runEventGeneration(CIUtilsBase):
    """Check Generator Datacards"""

    def __init__(self, workDirectory, outputDirectory):
        super().__init__(workDirectory, outputDirectory)

class runSummary(CIUtilsBase):
    """Run summary of all processes"""

    def __init__(self, workDirectory, outputDirectory):
        super().__init__(workDirectory, outputDirectory)
