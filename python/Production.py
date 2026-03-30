from abc import ABC,abstractmethod
import os
import sys
import subprocess
import shutil
from pathlib import Path
import filecmp

from Yaml2Datacard import Yaml2Datacard

class ProductionBase(ABC):
    """Base class for all k4GeneratorConfig operations"""
    def __init__(self, args):

        # consistent processing of names
        self._workDir = os.getcwd()+"/"+args.workDir
        if args.workDir.startswith('/'):
            self._workDir = args.workDir

        self._outDir = os.getcwd()+"/"+args.outputDir
        if args.outputDir.startswith('/'):
            self._outdir = args.outputDir

        self._referenceDir = os.getcwd()+"/"+args.refDir
        if args.refDir.startswith('/'):
            self._referenceDir = args.refDir

        self._generatorDir = f"{self._workDir}/{args.generatorDirName}"

    def getGenerators(self, generator):
        if generator == "All":
            return os.listdir(self._generatorDir)
        else:
            return [generator]

    def getProcesses(self, generator):
        return os.listdir(f"{self._generatorDir}/{generator}")

    def getFileNames(self, directory):
        filenames = os.listdir(directory)
        filenames =[name for name in filenames if os.path.isfile(os.path.join(directory,name))]
        return filenames

    def makeDirectory(self, dirname, overwrite=True):
        # Overwrite directory if it exists
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        else:
            if overwrite:
                shutil.rmtree(dirname)
                os.makedirs(dirname)

    def makeOutputDirectory(self, generator, process):
        if generator not in os.listdir(self._outDir):
            self.makeDirectory(f"{self._outDir}/{generator}")
        if process not in os.listdir(f"{self._outDir}/{generator}"):
            self.makeDirectory(f"{self._outDir}/{generator}/{process}")

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

class makeGeneratorDatacards(ProductionBase):
    """Generator Generator Datacards"""

    def __init__(self, args):
        super().__init__(args)

        # make the directory for the work, protect against "./"
        self.makeDirectory(args.workDir, not (os.path.abspath(args.workDir) == os.getcwd() ))
        # make the output directory for the output
        self.makeDirectory(args.outputDir, not (os.path.abspath(args.outputDir) == os.getcwd() ))

        # the sqrts argument can be a list of sqrts or a list of strings
        sqrtsGlobalFileName = str("")
        if len(args.sqrts) > 0:
            try:
                all(float(val) for val in args.sqrts)
                # write the values to a file
                try:
                    sqrtsGlobalFileName = f"{self._workDir}/sqrts.yaml"
                    sqrtsFile = open(sqrtsGlobalFileName,"x")
                    sqrtsList = "ecms: [ "
                    for sqrts in args.sqrts:
                        sqrtsList += f" {sqrts},"
                    sqrtsFile.write(sqrtsList.rstrip(",") + "]")
                    sqrtsFile.close()
                except FileExistsError as e:
                    sys.exit(f"Command line specification --sqrts with a {args.sqrts} triggers writing of {sqrtsGlobalFileName}, but file exists")
            except ValueError as e:
                if len(args.sqrts) == 1:
                    if Path(args.sqrts[0]).stem+Path(args.sqrts[0]).suffix == "sqrts.yaml" and os.path.isfile(args.sqrts[0]):
                        sqrtsGlobalFileName = os.path.abspath(args.sqrts[0])

        # specific members for DC creation
        self._yamlFiles  = []
        self._sqrtsFiles = []

        # prepare yamls:
        self.prepareYamls(args.yaml);

        # prepare the Sqrts files if global is not set
        if not sqrtsGlobalFileName:
            self.prepareSQRTS(args.sqrts);

        # args modifiable:
        self.Yaml2DatacardArgs = args
        
        # run all yamls:
        self.run(sqrtsGlobalFileName);

        # move the output to storage
        generators = self.getGenerators("All")
        # now compare to reference
        self.process(generators)

    def execute(self, generator, process):

        self.makeOutputDirectory(generator, process)
        outDir = f"{self._outDir}/{generator}/{process}"

        genProcDir = f"{self._generatorDir}/{generator}/{process}"
        fileNames = self.getFileNames(genProcDir)

        success = True
        for name in fileNames:
            theFile = f"{genProcDir}/{name}"
            try:
                shutil.copy(theFile, outDir)
            except:
                print(f"{theFile} could not be copied to {outDir}")
                success= False

        return success

    def prepareYamls(self, yamlList):
        # check whether this is a list of directories or mixed or files
        yamlDirs = []
        for yaml in yamlList:
            if os.path.isfile(yaml) and yaml.endswith('.yaml') and not Path(yaml).stem.startswith('sqrts'):
                self._yamlFiles.append(os.path.abspath(yaml))
            elif os.path.isdir(yaml):
                yamlDirs.append(os.path.abspath(yaml))
                
        # now we have a list of directories and a list of yaml files, extend the list of yaml files in the directories
        for yamlDir in yamlDirs:
            for filename in os.listdir(yamlDir):
                if filename.endswith('.yaml') and not filename.startswith('sqrts'):
                    self._yamlFiles.append(f"{yamlDir}/{filename}")

    def prepareSQRTS(self, sqrtsList):
        # check whether this is a list of directories or mixed or files
        sqrtsDirs = []
        for sqrts in sqrtsList:
            if os.path.isfile(sqrts) and Path(sqrts).stem.startswith('sqrts') and sqrts.endswith('.yaml'):
                self._sqrtsFiles.append(os.path.abspath(sqrts))
            elif os.path.isdir(sqrts):
                sqrtsDirs.append(os.path.abspath(sqrts))

        # now we have a list of directories and a list of sqrts files, extend the list of sqrts files in the directories
        for sqrtsDir in sqrtsDirs:
            for filename in os.listdir(sqrtsDir):
                if filename.startswith('sqrts') and filename.endswith('.yaml'):
                    self._sqrtsFiles.append(f"{sqrtsDir}/{filename}")

    def run(self, sqrtsGlobal):
        # remember where we start from
        cwd = os.getcwd()
        # go to the working directory
        os.chdir(self._workDir)
        # loop over all files
        for filename in self._yamlFiles:

            # check SQRTS: priority: global then comparison with filenames for specific processes 
            processName = Path(filename).stem
            sqrtsName   = f"{Path(filename).parent}/sqrts{processName}.yaml"
            if sqrtsGlobal:
                sqrtsName = sqrtsGlobal
            else:
                if not any( name == sqrtsName for name in self._sqrtsFiles):
                    sqrtsName = ""
            # everything is prepared, we can run now
            self.Yaml2DatacardArgs.inputfiles = [filename]
            message     = f"Processing : {processName} from file {self.Yaml2DatacardArgs.inputfiles}"
            if sqrtsName and os.path.isfile(sqrtsName):
                self.Yaml2DatacardArgs.sqrts      = sqrtsName
                message += f"{message} with {self.Yaml2DatacardArgs.sqrts}"
            print(message)
            Yaml2Datacard(self.Yaml2DatacardArgs)
        # return to the starting point
        os.chdir(cwd)

class checkGeneratorDatacards(ProductionBase):
    """Check Generator Datacards"""

    def __init__(self, args):
        super().__init__(args)

        # retrieve all generators in the workdirector:
        generators = self.getGenerators(args.generator)

        # now compare to reference
        self.process(generators)

    def execute(self, generator, process):
        genProc = f"{generator}/{process}"
        newDir = f"{self._generatorDir}/{genProc}"
        refDir = f"{self._referenceDir}/{genProc}"
        fileNames = self.getFileNames(newDir)

        success = True
        # check that all files were created (new) and are available for comparison (ref)
        if len(fileNames) != len(self.getFileNames(refDir)):
            print(f"Number of files for Generator {generator} process {process} differ between reference {len(fileNames)} and creation {len(self.getFileNames(refDir))}")
            success = False

        for name in fileNames:
            newFile = f"{newDir}/{name}"
            # new file must exist
            if  not os.path.isfile(newFile):
                print(f"File {newFile} not found")
                success = False
                continue

            refFile = f"{refDir}/{name}"
            # reference file must exist
            if not os.path.isfile(refFile):
                print(f"File {refFile} not found")
                continue
                success = False

            # both files exist, so we can compare
            message = f"Generator {generator} Process {process} File {name}"
            if filecmp.cmp(refFile,newFile, shallow=False):
                print(f"{message} identical")
            else:
                print(f"{message} differ")
                success = False

        return success

class generate(ProductionBase):
    """Run Event Generation"""

    def __init__(self, args):
        super().__init__(args)

        # retrieve all generators in the workdirector:
        generators = self.getGenerators(args.generator)

        # now compare to reference
        self.process(generators)

    def execute(self, generator, process):
        # go to the directory
        genProcDir = f"{self._generatorDir}/{generator}/{process}"
        os.chdir(genProcDir)
        # retrieve the script
        scripts = [script for script in os.listdir(genProcDir) if script.startswith('Run_') and script.endswith('.sh')]
        if len(scripts) != 1:
            print(f"Found more than one script for generator {generator} with process {process}")
            return False
        # execute
        success = True
        for script in scripts:
            try:
                result = subprocess.run(f"./{script}", capture_output=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Execution error for {generator} in process {process}")
                print(e.returncode)
                print(e.output)
                success = False

        self.makeOutputDirectory(generator, process)
        outDir = f"{self._outDir}/{generator}/{process}"
        fileNames = [filename for filename in self.getFileNames(genProcDir) if filename.endswith('.edm4hep')]
        for name in fileNames:
            theFile = f"{genProcDir}/{name}"
            try:
                shutil.copy(theFile, outDir)
            except:
                print(f"{theFile} could not be copied to {outDir}")
                success= False

        return success

class summary(ProductionBase):
    """Make a summary of all processes"""

    def __init__(self, args):
        super().__init__(args)

        print("Extracting the cross sections by reading EDM4HEP files and superposing the differential distributions")
        # remember where we start from
        cwd = os.getcwd()
        os.chdir(self._workDir)
        try:
            result = subprocess.run(["eventGenerationSummary",
                                     "-w", f"{self._generatorDir}",
                                     "-f", f"{self._outDir}/GenerationSummary.dat",
                                     "-d", f"{self._outDir}"],
                                     capture_output=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Execution error eventGenerationSummary")
            print(e.returncode)
            print(e.output.decode("utf-8"))
            sys.exit("Exception thrown by eventGenerationSummary")

        # return tu the starting point
        os.chdir(cwd)

    def execute(self, generator, process):
        pass
