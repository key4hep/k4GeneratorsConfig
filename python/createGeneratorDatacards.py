import os
import sys
import shutil
from pathlib import Path

from main import main

class createGeneratorDatacards:
    """Generator Generator Datacards"""

    def __init__(self, yamlDirectory, yamlFile, workDirectory, outputDirectory):
        # useful for the class
        self._yamlDir  = yamlDirectory
        self._yamlFiles = []
        self._workDir  = workDirectory
        self._outDir   = outputDirectory

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
            self._yamlFiles =[yamlFile]

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
