#!/usr/bin/env python3

import os
import sys
import argparse
import textwrap
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

        ReleaseSpec.set_info("key4hepUseNightlies",args.key4hepUseNightlies)
        if ReleaseSpecs.key4hepUseNightlies.value:
            print(f"key4HEP configuration: NIGHTLIES")
        else:
            print(f"key4HEP configuration: RELEASE")

        # make sure it's a valid date
        if args.key4hepVersion is not None:
            try:
                relDate = datetime.strptime(args.key4hepVersion,'%Y-%m-%d')
                if (datetime.today() - relDate).days < 0:
                    raise ValueError()
                print(f"key4HEP configuration date: {args.key4hepVersion}")
            except ValueError:
                print(f"Invalid KEY4HEP release argument, YYYY-MM-DD expected, latest possible date {datetime.today().strftime('%Y-%m-%d')}")
                print(f"Requested: {args.key4hepVersion}")
                print("Cannot configure scripts correctly, exiting")
                exit()
        else:
            print(f"key4HEP configuration date: latest")
        # store for future use:
        ReleaseSpec.set_info("key4hepReleaseDate",args.key4hepVersion)

        # sqrts choices from file
        energies = [0.]
        if args.sqrts:
            sqrtsReader = Reader.SQRTSReader(args.sqrts)
            energies = sqrtsReader.energies()

        # now we read the global settings
        try:
            # make sure that we follow a symlink to the real location of the parametersets should replace that by share?
            parameterSet = Reader.ParameterSetReader(args.parameterTagFile, args.parameterTag)
        except FileNotFoundError as e:
            print(f"ERROR: File {e} with parameters for tag {args.parameterTag} not found")
            exit()

        # execute file processes
        rndmSeed = args.seed
        for sqrts in energies:
            rndmIncrement = self.executeFiles(args, sqrts, rndmSeed)
            # offset for next round by number of yaml files
            rndmSeed = rndmSeed + rndmIncrement

    def executeFiles(self, args, sqrts, rndmSeedFallback):
        # remember where we started from:
        cwd = os.getcwd()
        # first step reset all particles:
        ParticleCollection()
        # read the input file
        self.processReader = Reader.ProcessReader(args.yaml, sqrts)
        # set the number of events if present
        if args.nevts != -1:
            self.processReader.set("events", events)
        # the datacard outputDir may differ
        self.processOutputDir(args)
        # now extract information
        processes        = self.processReader.get_processes(sqrts)
        yamlParticleData = self.processReader.get_particle_data()
        generators       = Generators(self.processReader)
        #
        rndmIncrement = 0
        for key, value in processes.items():
            self.makeDirectories4GeneratorsProcess(self.processReader.get_generators(), key)
            try:
                randomseed = value["randomseed"]
            except:
                randomseed = rndmSeedFallback + rndmIncrement
                value["randomseed"] = randomseed
                rndmIncrement += 1
            param = ProcessParameters(self.processReader)
            # instantiate the class for each process
            process = Process(
                value, key, param, yamlParticleData, OutDir=self.outputDir
            )
            process.prepareProcess()
            generators.runGeneratorConfiguration(process)
        # at the end back to the starting point dir for the next file
        if (cwd != os.getcwd()):
            os.chdir(cwd)

        return rndmIncrement

    def processOutputDir(self, args):
        # the output directory
        self.outputDir = getattr(self.processReader, "outdir", args.outputDir)
        if args.outputDirOverride:
            self.outputDir = args.outputDir
        # the attribute always has to be reset to be sure....
        setattr(self.processReader, "outdir", args.outputDir)
        # all the preparatory work has been done in args.outputDir
        # create the new directory if it does not exist
        if not args.outputDirOverride:
            if not os.path.exists(self.outputDir):
                os.makedirs(self.outputDir)
            os.chdir(self.outputDir)

    def makeDirectories4GeneratorsProcess(self, generators, procname):
        # do not overwrite directory if it exists
        for generator in generators:
            process_directory = os.path.join(generator, procname)
            if not os.path.exists(process_directory):
                os.makedirs(process_directory)

if __name__ == "__main__":
    Yaml2Datacard()
