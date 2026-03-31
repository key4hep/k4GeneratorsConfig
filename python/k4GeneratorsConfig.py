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

def k4GeneratorsConfig(arguments=None):
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
    parser.add_argument(
        "--workDir",
        type=str,
        default="work",
        help="path to work directory (default: ./work)"
    )
    parser.add_argument(
        "--outputDir",
        type=str,
        default="output",
        help="path to the output (default: ./output)"
    )
    parser.add_argument(
        "--generatorDirName",
        type=str,
        default="Run-Cards",
        help="relative path to the Generator directories in outputDir (default: outputDir/Run-Cards)"
    )
    parser.add_argument(
        "--all",
        action='store_true',
        help="activates --make --generate --summary"
    )

    args = parser.parse_args(arguments)
    # --all overrides --make --generate --summary
    if args.all:
        args.make     = True
        args.generate = True
        args.summary  = True
        print("k4GeneratorsConfig will make generator datacards, generate events, make a summary")

    if args.make:
        makeGeneratorDatacards(args)

    if args.check:
        checkGeneratorDatacards(args)

    if args.generate:
        generate(args)

    if args.summary:
        summary(args)

if __name__ == "__main__":
    k4GeneratorsConfig()

