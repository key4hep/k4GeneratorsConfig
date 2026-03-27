#!/usr/bin/env python3

import os
import shutil
import sys
import argparse
import textwrap

from createGeneratorDatacards import createGeneratorDatacards

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

    yamlDirectory  = os.path.dirname(os.path.realpath(__file__))+"/"+args.yamlDir
    if args.yamlDir.startswith("/"):
        yamlDirectory = args.yamlDir

    yamlFile       = "None"
    if args.yamlFile != "None":
        yamlFile       = yamlDirectory+"/"+args.yamlFile

    workDirectory  = os.path.dirname(os.path.realpath(__file__))+"/"+args.workDir
    if args.workDir.startswith("/"):
        workDirectory = args.workDir

    outputDirectory  = os.path.dirname(os.path.realpath(__file__))+"/"+args.outputDir
    if args.outputDir.startswith("/"):
        outputDirectory = args.outputDir

    if args.create:
        createGeneratorDatacards(yamlDirectory,yamlFile,workDirectory,outputDirectory)

    #if args.check:
        #checkGeneratorDatacards()

    #if args.run:
        #runEventGeneration()

    #if args.summary:
        #runSummary()

if __name__ == "__main__":
    run()

