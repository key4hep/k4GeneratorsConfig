#!/usr/bin/env python3

import os
import shutil
import sys
import argparse
import textwrap

from Production import makeGeneratorDatacards
from Production import checkGeneratorDatacards
from Production import generate
from Production import summary

class k4GeneratorsConfig():
    def __init__(self,arguments=None):
        parser = argparse.ArgumentParser(prog="k4GeneratorsConfig")
        parser.add_argument(
            "--make",
            action='store_true',
            help="make the generator datacards from the yaml files"
        )
        parser.add_argument(
            "--yaml",
            nargs="*",
            type=str,
            default=[os.path.dirname(os.path.realpath(__file__))+'/../examples'],
            help="yamlFiles and director(y/ies) with yaml files (default: k4GeneratorsConfig/examples)"
        )
        parser.add_argument(
            "--sqrts",
            nargs="*",
            type=str,
            default=[],
            help="either a space separated list of center of mass energies OR file(s) and director(y/ies) with sqrts lists in yaml format (name : sqrtsPROCESS.dat containing eg, sqrts:[91.,240.]),  sqrts.yaml as single argument will be applied to all processes",
        )
        parser.add_argument(
            "--seed",
            nargs=1,
            type=int,
            default=4711,
            help="initial random number seed, increment for each file",
        )
        parser.add_argument(
            "--nevts",
            type=int,
            default=-1,
            help="Number of events to be generated",
        )
        parser.add_argument(
            "--parameterTag",
            type=str,
            default="latest",
            help="parameter tag in Parameters.yaml (default: latest)",
        )
        parser.add_argument(
            "--parameterTagFile",
            type=str,
            default=os.path.dirname(os.path.realpath(__file__))+'/ParameterSets.yaml',
            help="name of file containing the parameter sets of the requested parameterTag, default: ParameterSets.yaml in directory: k4GeneratorsConfig/python",
        )
        parser.add_argument(
            "--key4hepUseNightlies",
            action='store_true',
            help="configures the key4hepscripts to use nightlies instead of releases",
        )
        parser.add_argument(
            "--key4hepVersion",
            default=None,
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
        self.outputDirDefault = "work"
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
        self.checkArguments(args)
        # make the GeneratorDatacards
        if args.make:
            makeGeneratorDatacards(args)
        # compare to the reference
        if args.check:
            checkGeneratorDatacards(args)
        # run the event generation
        if args.generate:
            generate(args)
        # produce the summary
        if args.summary:
            summary(args)

    def checkArguments(self, args):

        # OPTION: outputDir
        # differentiate between option being given or not
        try:
            check = args.outputDir
            args.outputDirOverride = True
        except AttributeError:
            # argument was not given, set the default and make it known:
            args.outputDir          = self.outputDirDefault
            args.outputDirOverride = False
            # --all overrides --make --generate --summary
            if args.all:
                args.make     = True
                args.generate = True
                args.summary  = True
                print("k4GeneratorsConfig will make generator datacards, generate events, make a summary")
        # outputDir should never be cwd
        if ( os.path.abspath(args.outputDir) == os.path.abspath(os.getcwd()) ):
            message = f"k4GeneratorsConfig::ERROR --outputDir {args.outputDir} not allowed \nPlease specify a directory other than the working directory"
            sys.exit(message)

        # OPTION all or make&&generate&&summary
        if ( args.all or
             (args.make and args.check) or
             (args.make and args.generate) or
             (args.make and args.summary) ):
            if not args.outputDirOverride:
                message = f"k4GeneratorsConfig::ERROR\n"
                message += f"--make and (--check and/or --generate and/or --summary) requested\n"
                message += f"yamlFiles may define multiple outputDirectory, functionality not foreseen\n"
                message += f"BUT: --outputDir {args.outputDir} not defined \nPlease define a common output directory"
                sys.exit(message)

if __name__ == "__main__":
    k4GeneratorsConfig()

