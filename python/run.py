#!/usr/bin/env python3

import os
import shutil
import sys
import argparse
import textwrap

from CIUtils import createGeneratorDatacards
from CIUtils import checkGeneratorDatacards

def run():
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
        help="create the generator datacards from the yaml files",
    )
    parser.add_argument(
        "--yamlDir",
        type=str,
        default="../examples",
        help="directory where the yamlFiles are located default: k4GeneratorsConfig/examples",
    )
    parser.add_argument(
        "--yamlFile",
        type=str,
        default="None",
        help="name of file to be processed default: all found in the yamlDir",
    )
    parser.add_argument(
        "--check",
        action='store_true',
        help="check the generator datacards with respect to the reference in k4GeneratorsConfig/test/ref-results",
    )
    parser.add_argument(
        "--generator",
        type=str,
        default="All",
        help="generator to be run, default: All",
    )
    parser.add_argument(
        "--run",
        action='store_true',
        help="run the event generation",
    )
    parser.add_argument(
        "--summary",
        action='store_true',
        help="compare the results of the event generation process by process",
    )
    parser.add_argument(
        "--workDir",
        type=str,
        default="../test/work",
        help="directory where the Work is performed default: k4GeneratorsConfig/test/work",
    )
    parser.add_argument(
        "--outputDir",
        type=str,
        default="../test/output",
        help="directory where the output is stored default: k4GeneratorsConfig/test/output",
    )

    args           = parser.parse_args()

    if args.create:
        createGeneratorDatacards(args.yamlDir,args.yamlFile,args.workDir,args.outputDir)

    if args.check:
        checkGeneratorDatacards(args.generator,args.workDir,args.outputDir)

    if args.run:
        runEventGeneration(args.workDir,args.outputDir)

    if args.summary:
        runSummary(args.workDir,args.outputDir)

if __name__ == "__main__":
    run()

