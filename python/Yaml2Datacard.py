#!/usr/bin/env python3

import os
import sys
import argparse
import textwrap
import copy
from datetime import datetime

import ReleaseSpecs
from ReleaseSpecs import ReleaseSpec
import YamlInputReader as Reader
from Process import Process
from Process import ProcessParameters
from Generators import Generators
from Particles import ParticleCollection

class Yaml2Datacard:
    """Convert Input files into generator datacards"""

    def __init__(self,args):
        # copy the arguments
        self.args = copy.deepcopy(args)

        ReleaseSpec.set_info("key4hepUseNightlies",self.args.key4hepUseNightlies)
        if ReleaseSpecs.key4hepUseNightlies.value:
            print(f"key4HEP configuration: NIGHTLIES")
        else:
            print(f"key4HEP configuration: RELEASE")

        # make sure it's a valid date
        if self.args.key4hepVersion is not None:
            try:
                relDate = datetime.strptime(self.args.key4hepVersion,'%Y-%m-%d')
                if (datetime.today() - relDate).days < 0:
                    raise ValueError()
                print(f"key4HEP configuration date: {self.args.key4hepVersion}")
            except ValueError:
                print(f"Invalid KEY4HEP release argument, YYYY-MM-DD expected, latest possible date {datetime.today().strftime('%Y-%m-%d')}")
                print(f"Requested: {self.args.key4hepVersion}")
                print("Cannot configure scripts correctly, exiting")
                exit()
        else:
            print(f"key4HEP configuration date: latest")
        # store for future use:
        ReleaseSpec.set_info("key4hepReleaseDate",self.args.key4hepVersion)

        # sqrts choices from file
        self.energies = [0.]
        if self.args.sqrts:
            sqrtsReader = Reader.SQRTSReader(self.args.sqrts)
            self.energies = sqrtsReader.energies()

        # now we read the global settings
        try:
            # make sure that we follow a symlink to the real location of the parametersets should replace that by share?
            parameterSet = Reader.ParameterSetReader(self.args.parameterTagFile, self.args.parameterTag)
        except FileNotFoundError as e:
            exit(f"ERROR: File {e} with parameters for tag {self.args.parameterTag} not found"f"ERROR: File {e} with parameters for tag {self.args.parameterTag} not found")

    def processFile(self):
        # execute file processes
        rndmSeed = self.args.seed
        for sqrts in self.energies:
            # remember where we started from:
            cwd = os.getcwd()
            # first step reset all particles:
            ParticleCollection()
            # read the input file
            self.processReader = Reader.ProcessReader(self.args.yaml, sqrts)
            # set the number of events if present
            if self.args.nevts != -1:
                self.processReader.set("events", events)
            # the datacard outputDir may differ
            self.processOutputDir()
            # now extract information
            processes        = self.processReader.get_processes(sqrts)
            yamlParticleData = self.processReader.get_particle_data()
            generators       = Generators(self.processReader)
            #
            for key, value in processes.items():
                self.makeDirectories4GeneratorsProcess(self.processReader.get_generators(), key)
                try:
                    randomseed = value["randomseed"]
                except:
                    # random seed not present, fall to external setting and increment for next round
                    value["randomseed"] = rndmSeed
                    rndmSeed += 1
                param = ProcessParameters(self.processReader)
                # instantiate the class for each process
                process = Process(
                    value, key, param, yamlParticleData, OutDir=self.outputDir
                )
                process.prepareProcess()
                generators.runGeneratorConfiguration(process)

            # increment for next sqrts
            rndmSeed += 1
            
            # at the end back to the starting point dir for the next file
            if (cwd != os.getcwd()):
                os.chdir(cwd)

    def processOutputDir(self):
        # the output directory
        self.outputDir = getattr(self.processReader, "outdir", self.args.outputDir)
        if self.args.outputDirOverride:
            self.outputDir = self.args.outputDir
        # the attribute always has to be reset to be sure....
        setattr(self.processReader, "outdir", self.args.outputDir)
        # all the preparatory work has been done in self.args.outputDir
        # create the new directory if it does not exist
        if not self.args.outputDirOverride:
            try:
                if not os.path.exists(self.outputDir):
                    os.makedirs(self.outputDir)
            except PermissionError:
                message = f"Yaml2Datacard::processOutputDir::ERROR:\n{self.outputDir} cannot be created (full path: {os.path.abspath(self.outputDir)})"
                sys.exit(message)
            os.chdir(self.outputDir)

    def makeDirectories4GeneratorsProcess(self, generators, procname):
        # do not overwrite directory if it exists
        for generator in generators:
            process_directory = os.path.join(generator, procname)
            if not os.path.exists(process_directory):
                try:
                    os.makedirs(process_directory)
                except PermissionError:
                    message = f"Yaml2Datacard::makeDirectories4GeneratorsProcess::ERROR:\n{process_directory} cannot be created (full path: {os.path.abspath(process_directory)})"
                    sys.exit(message)

if __name__ == "__main__":
    Yaml2Datacard()
