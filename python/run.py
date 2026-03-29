#!/usr/bin/env python3

import os
import shutil
import sys
import argparse
import textwrap

from CIUtils import createGeneratorDatacards
from CIUtils import checkGeneratorDatacards
from CIUtils import runEventGeneration
from CIUtils import runSummary

def run(arguments=None):
    parser = argparse.ArgumentParser(
        prog="k4GeneratorsConfig",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """\
The following options are available:
------------------------------------
    """
        ),
    )
    parser.add_argument(
        "--create",
        action='store_true',
        help="create the generator datacards from the yaml files"
    )
    parser.add_argument(
        "--yamlDir",
        type=str,
        default="../examples",
        help="path to the yamlFiles (default: k4GeneratorsConfig/examples)"
    )
    parser.add_argument(
        "--yamlFiles",
        type=str,
        nargs="+",
        default="",
        help="yamlfiles to be processed (default: all are processed)"
    )
    parser.add_argument(
        "--check",
        action='store_true',
        help="check the generator datacards with respect to the reference"
    )
    parser.add_argument(
        "--refDir",
        type=str,
        default="../test/ref-results",
        help="path to the reference files (default: k4GeneratorsConfig/test/ref-results)"
    )
    parser.add_argument(
        "--generator",
        type=str,
        default="All",
        help="generator to be run (default: All processed)"
    )
    parser.add_argument(
        "--run",
        action='store_true',
        help="run the event generation step"
    )
    parser.add_argument(
        "--summary",
        action='store_true',
        help="compare the results of the event generation process by process and produce summary output in outputDir"
    )
    parser.add_argument(
        "--workDir",
        type=str,
        default="../test/work",
        help="path to work directory (default: k4GeneratorsConfig/test/work)"
    )
    parser.add_argument(
        "--outputDir",
        type=str,
        default="../test/output",
        help="path to the output (default: k4GeneratorsConfig/test/output)"
    )
    parser.add_argument(
        "--generatorDirName",
        type=str,
        default="Run-Cards",
        help="relative path to the Generator directories (default: outputDir/generatorDirName)"
    )

    args = parser.parse_args(arguments)

    if args.create:
        createGeneratorDatacards(args)

    if args.check:
        checkGeneratorDatacards(args)

    if args.run:
        runEventGeneration(args)

    if args.summary:
        runSummary(args)

if __name__ == "__main__":
    run()

