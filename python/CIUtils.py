from abc import ABC,abstractmethod
import os
import sys
import subprocess
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

        self._outDir = os.path.dirname(os.path.realpath(__file__))+"/"+outputDirectory
        if outputDirectory.startswith("/"):
            self.outdir = outputDirectory

        self._referenceDir = os.path.dirname(os.path.realpath(__file__))+"/../test/ref-results"

        self._generatorDir = self._workDir+"/Run-Cards"

    def getGenerators(self, generator):
        if generator == "All":
            return os.listdir(self._generatorDir)
        else:
            return [generator]

    def getProcesses(self, generator):
        return os.listdir(self._generatorDir+"/"+generator)

    def getFileNames(self, directory):
        filenames = os.listdir(directory)
        filenames =[name for name in filenames if os.path.isfile(os.path.join(directory,name))]
        return filenames

    def process(self, generators):
        # where do we start from
        cwd = os.getcwd()

        failure = False
        for generator in generators:
            processes = self.getProcesses(generator)

            for process in processes:
                if not self.execute(generator, process):
                    failure = True

        if failure:
            sys.exit("Failed")
        # return to the starting point
        os.chdir(cwd)

    @abstractmethod
    def execute(self, generator, process):
        pass

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

        # run all yamls:
        self.run();

        # move the output to storage
        generators = self.getGenerators("All")
        # now compare to reference
        self.process(generators)
        

    def execute(self, generator, process):

        if generator not in os.listdir(self._outDir):
            self.makeDirectory(f"{self._outDir}/{generator}")
        if process not in os.listdir(f"{self._outDir}/{generator}"):
            self.makeDirectory(f"{self._outDir}/{generator}/{process}")
        outDir = f"{self._outDir}/{generator}/{process}"

        genProc = "/"+generator+"/"+process
        genProcDir = self._generatorDir+genProc
        fileNames = self.getFileNames(genProcDir)

        success = True
        for name in fileNames:
            theFile = genProcDir+"/"+name
            try:
                shutil.copy(theFile, outDir)
            except:
                print(f"{theFile} could not be copied to {outDir}")
                success= False

        return success

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

    def run(self):
        # remember where we start from
        cwd = os.getcwd()
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
        # return tu the starting point
        os.chdir(cwd)

class checkGeneratorDatacards(CIUtilsBase):
    """Check Generator Datacards"""

    def __init__(self, generator, workDirectory, outputDirectory):
        super().__init__(workDirectory, outputDirectory)

        # retrieve all generators in the workdirector:
        generators = self.getGenerators(generator)

        # now compare to reference
        self.process(generators)

    def execute(self, generator, process):
        genProc = "/"+generator+"/"+process
        newDir = self._generatorDir+genProc
        refDir = self._referenceDir+genProc
        fileNames = self.getFileNames(refDir)

        success = True
        for name in fileNames:
            newFile = newDir+"/"+name
            refFile = refDir+"/"+name
            message = "Generator "+generator+" Process "+process+" File "+name
            if filecmp.cmp(refFile,newFile, shallow=False):
                print(message+" identical")
            else:
                print(message+" differ")
                success = False

        return success

class runEventGeneration(CIUtilsBase):
    """Run Event Generation"""

    def __init__(self, generator, workDirectory, outputDirectory):
        super().__init__(workDirectory, outputDirectory)

        # retrieve all generators in the workdirector:
        generators = self.getGenerators(generator)

        # now compare to reference
        self.process(generators)

    def execute(self, generator, process):
        # go to the directory
        genProcDir = self._generatorDir+"/"+generator+"/"+process
        os.chdir(genProcDir)
        # retrieve the script
        scripts = [script for script in os.listdir(genProcDir) if script.startswith("Run_") and script.endswith(".sh")]
        if len(scripts) != 1:
            print(f"Found more than one script for generator {generator} with process {process}")
            return False
        # execute
        success = True
        for script in scripts:
            try:
                result = subprocess.run("./"+script, capture_output=True, check=True)
            except CalledProcessError:
                print(f"Execution error for {generator} in process {process}")
                print(result.stdout)
                print(result.stderr)
                success = False

        return success

class runSummary(CIUtilsBase):
    """Run summary of all processes"""

    def __init__(self, workDirectory, outputDirectory):
        super().__init__(workDirectory, outputDirectory)

        print("Extracting the cross sections by reading EDM4HEP files and superposing the differential distributions")
        
        try:
            result = subprocess.run(["eventGenerationSummary",
                                     "-f", f"{self._outDir}}/GenerationSummary.dat",
                                     "-d", "../output",
                                     capture_output=True, check=True)
        except CalledProcessError:
            print(f"Execution error eventGenerationSummary")
            print(result.stdout)
            print(result.stderr)
