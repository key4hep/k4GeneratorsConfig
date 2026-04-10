#!/usr/bin/env python3

import os
import shutil
import sys
import argparse
import textwrap
import copy

from Production import makeGeneratorDatacards
from Production import checkGeneratorDatacards
from Production import generate
from Production import summary

class k4GeneratorsConfig():
    def __init__(self,arguments=None):
        # define all command line arguments
        parser = argparse.ArgumentParser(prog="k4GeneratorsConfig")

        parser.add_argument(
            "--make",
            action='store_true',
            help="make the generator datacards from the yaml files"
        )

        self.yamlDefault = [os.path.dirname(os.path.realpath(__file__))+'/../examples']
        parser.add_argument(
            "--yaml",
            nargs="*",
            type=str,
            default=argparse.SUPPRESS,
            help="yamlFiles and director(y/ies) with yaml files (default: k4GeneratorsConfig/examples)"
        )

        self.sqrtsDefault = []
        parser.add_argument(
            "--sqrts",
            nargs="*",
            type=str,
            default=argparse.SUPPRESS,
            help="either a space separated list of center of mass energies OR file(s) and director(y/ies) with sqrts lists in yaml format (name : sqrtsPROCESS.dat containing eg, sqrts:[91.,240.]),  sqrts.yaml as single argument will be applied to all processes",
        )

        self.seedDefault = 4711
        parser.add_argument(
            "--seed",
            type=int,
            default=argparse.SUPPRESS,
            help="If specified overrides the random number seed in the yamlFile, incremented for each process and each sqrts of a yaml file, default: yaml file",
        )

        self.nevtsDefault = -1
        parser.add_argument(
            "--nevts",
            type=int,
            default=argparse.SUPPRESS,
            help="If specified overrides the number of events to be generated in the yamlFile, default: use yaml",
        )

        self.parameterTagDefault = "latest"
        parser.add_argument(
            "--parameterTag",
            type=str,
            default=argparse.SUPPRESS,
            help="parameter tag in Parameters.yaml (default: latest)",
        )

        self.parameterTagFileDefault = os.path.dirname(os.path.realpath(__file__))+'/ParameterSets.yaml'
        parser.add_argument(
            "--parameterTagFile",
            type=str,
            default=argparse.SUPPRESS,
            help="name of file containing the parameter sets of the requested parameterTag, default: ParameterSets.yaml in directory: k4GeneratorsConfig/python",
        )

        parser.add_argument(
            "--key4hepUseNightlies",
            action='store_true',
            help="configures the key4hepscripts to use nightlies instead of releases",
        )

        self.key4hepVersionDefault = None
        parser.add_argument(
            "--key4hepVersion",
            default=argparse.SUPPRESS,
            help="force the use of the version : YYYY-MM-DD (default: latest)",
        )
        parser.add_argument(
            "--check",
            action='store_true',
            help="check the generator datacards with respect to the reference"
        )
        parser.add_argument(
            "--refDir",
            type=str,
            default=os.path.dirname(os.path.realpath(__file__))+'/../test/ref-results',
            help="path to the reference files (default: k4GeneratorsConfig/test/ref-results)"
        )
        parser.add_argument(
            "--generator",
            type=str,
            default="All",
            help="generator to be run (default: All processed)"
        )
        parser.add_argument(
            "--generate",
            action='store_true',
            help="run the event generation"
        )
        parser.add_argument(
            "--summary",
            action='store_true',
            help="compare the results of the event generation process by process and produce summary output in outputDir"
        )

        self.outputDirDefault = "Run-Cards"
        parser.add_argument(
            "--outputDir",
            type=str,
            default=argparse.SUPPRESS,
            help=f"path to output directory (default: ./{self.outputDirDefault}, if specified, overrides the outdir key in yaml)"
        )
        parser.add_argument(
            "--all",
            action='store_true',
            help="activates --make --generate --summary"
        )

        # decode the arguments
        args = parser.parse_args(arguments)
        # check the arguments
        self.processArguments(args)
        # make the GeneratorDatacards
        if self.args.make:
            makeGeneratorDatacards(self.args)
        # compare to the reference
        if self.args.check:
            checkGeneratorDatacards(self.args)
        # run the event generation
        if self.args.generate:
            generate(self.args)
        # produce the summary
        if self.args.summary:
            summary(self.args)

    def processArguments(self, args):
        # make a deep copy of the arguments:
        self.args = copy.deepcopy(args)
        # OPTION: outputDir
        # differentiate between option being given or not
        try:
            check = args.outputDir
            self.args.outputDirOverride = True
        except AttributeError:
            # argument was not given, set the default and make it known:
            self.args.outputDir          = self.outputDirDefault
            self.args.outputDirOverride = False

        # --all overrides --make --generate --summary
        if args.all:
            self.args.make     = True
            self.args.generate = True
            self.args.summary  = True
            print("k4GeneratorsConfig will make generator datacards, generate events, make a summary")

        # outputDir should never be cwd
        if ( os.path.abspath(self.args.outputDir) == os.path.abspath(os.getcwd()) ):
            message = f"k4GeneratorsConfig::ERROR --outputDir {self.args.outputDir} not allowed \nPlease specify a directory other than the working directory"
            sys.exit(message)

        # OPTION all or make&&generate&&summary
        if ( args.all or
             (args.make and args.check) or
             (args.make and args.generate) or
             (args.make and args.summary) ):
            if not self.args.outputDirOverride:
                message = f"k4GeneratorsConfig::ERROR\n"
                message += f"--make and (--check and/or --generate and/or --summary) requested\n"
                message += f"yamlFiles may define multiple outputDirectory, functionality not foreseen\n"
                message += f"BUT: --outputDir {self.args.outputDir} not defined \nPlease define a common output directory"
                sys.exit(message)

        # make sure that Warnings are issued when options specific to --make are invoked, make is false
        message = "k4GeneratorsConfig::WARNING invoking option specific to --make or --all:"
        try:
            check = self.args.yaml
            if not args.make and not args.all:
                print(f"{message} --yaml {self.args.yaml} has no effect")
        except AttributeError as e:
            if args.make or args.all:
                self.args.yaml = self.yamlDefault
        try:
            check = self.args.sqrts
            if not args.make and not args.all:
                print(f"{message} --sqrts {self.args.sqrts} has no effect")
        except AttributeError as e:
            if args.make or args.all:
                self.args.sqrts = self.sqrtsDefault
        try:
            check = self.args.seed
            self.args.seedOverride = True
            if check <= 0:
                sys.exit(f"k4GeneratorsConfig::ERROR --seed {self.args.seed} specified, must be >0")
            if not args.make and not args.all:
                print(f"{message} --seed {self.args.seed} has no effect")
        except AttributeError as e:
            if args.make or args.all:
                self.args.seed = self.seedDefault
                self.args.seedOverride = False
        try:
            check = self.args.nevts
            if not args.make and not args.all:
                print(f"{message} --nevts {self.args.nevts} has no effect")
        except AttributeError as e:
            if args.make or args.all:
                self.args.nevts = self.nevtsDefault
        try:
            check = self.args.parameterTag
            if not args.make and not args.all:
                print(f"{message} --parameterTag {self.args.parameterTag} has no effect")
        except AttributeError as e:
            if args.make or args.all:
                self.args.parameterTag = self.parameterTagDefault
        try:
            check = self.args.parameterTagFile
            if not args.make and not args.all:
                print(f"{message} --parameterTagFile {self.args.parameterTagFile} has no effect")
        except AttributeError as e:
            if args.make or args.all:
                self.args.parameterTagFile = self.parameterTagFileDefault
        try:
            check = self.args.key4hepVersion
            if not args.make and not args.all:
                print(f"{message} --key4hepVersion {self.args.key4hepVersion} has no effect")
        except AttributeError as e:
            if args.make or args.all:
                self.args.key4hepVersion = self.key4hepVersionDefault

        # special treatment for nightlies storetrue
        if not args.make and not args.all and args.key4hepUseNightlies:
            print(f"k4GeneratorsConfig::WARNING invoking option specific to --make or --all : --key4hepUseNightlies has no effect")

if __name__ == "__main__":
    k4GeneratorsConfig()

