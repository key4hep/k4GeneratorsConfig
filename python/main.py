#!/usr/bin/env python3

import os
import sys
import argparse
import textwrap
from datetime import datetime

import ReleaseSpecs
from ReleaseSpecs import ReleaseSpec
import Input as Settings
import Process as process_module
import Generators as generators_module

def make_output_directory(generators, output_directory, procname):
    # Overwrite directory if it exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for generator in generators:
        generator_directory = os.path.join(output_directory, generator, procname)
        if not os.path.exists(generator_directory):
            os.makedirs(generator_directory)


def main():
    # parser = argparse.ArgumentParser(prog='k4gen',description='Process input YAML files.')
    parser = argparse.ArgumentParser(
        prog="k4GeneratorsConfig",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """\
Process input YAML files.
The following options are available:
------------------------------------
SqrtS        : float (center of mass energy)
ISRmode      : int (0: off, 1: on)
    OutputFormat : string (format output, available are hepmc2 and hepmc3)
OutDir       : string (output directory, default=$PWD/Run-Cards)
Events       : unsigned int (Number of Monte-Carlo events to be generated)
Processes    : see README A list of processes which runcards should be generated. Each process should have its own unique name
        Processes:
          Muon:
             Initial: [11, -11]
             Final: [13, -13]
             Order: [2,0]
                     NLO: lo/qcd/qed (optional, default: lo)
                     RandomSeed : unsigned int (specify a random seed, important when generating multiple files for the same process)
ParticleData : overwrite basic particle properties
        ParticleData:
          25:
            mass: 125
            width: 0

For MADGRAPH and Whizard only:
PolarisationDensity  : float ([-1 or 0 or 1,1 or 0 or -1]) default: [-1, 1]
PolarisationFraction : float ([0...1.,0....1.]), default [0,0]
Beamstrahlung        : string (name of accelerator: ILC, FCC, CLIC, C3, HALFHF) 
    """
        ),
    )
    parser.add_argument("inputfiles", nargs="+", type=str, help="Input YAML file")
    parser.add_argument(
        "--ecms",
        nargs="*",
        type=float,
        default=[],
        help="energies to be processed, overrides nominal yaml input file settings",
    )
    parser.add_argument(
        "--ecmsFiles",
        nargs="*",
        type=str,
        default=[],
        help="yaml files with energies format ecms: [energy1,....] ",
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
        help="parameter tag in Parameters.yaml default is: latest",
    )
    parser.add_argument(
        "--parameterTagFile",
        type=str,
        default=None,
        help="name of file containing the parameter sets of the requested parameterTag, default: ParameterSets.yaml in  directory: python",
    )
    parser.add_argument(
        "--key4hepUseNightlies",
        action='store_true',
        help="configures the key4hepscripts to use nightlies instead of releases",
    )
    parser.add_argument(
        "--key4hepVersion",
        default=None,
        help="force the use of the version in default is latest, format: YYYY-MM-DD",
    )
    args           = parser.parse_args()
    files          = args.inputfiles
    energies       = args.ecms
    ecmsfiles      = args.ecmsFiles
    rndmSeed       = args.seed
    events         = args.nevts
    paramTag       = args.parameterTag
    paramFileName  = args.parameterTagFile
    releaseDate    = args.key4hepVersion

    ReleaseSpec.set_info("key4hepUseNightlies",args.key4hepUseNightlies)
    if ReleaseSpecs.key4hepUseNightlies:
        print(f"key4HEP configuration: using nightlies")
    else:
        print(f"key4HEP configuration: using release")

    # make sure it's a valid date
    if releaseDate is not None:
        try:
            relDate = datetime.strptime(releaseDate,'%Y-%m-%d')
            if (datetime.today() - relDate).days < 0:
                raise ValueError()
            print(f"key4HEP configuration date: {releaseDate}")
        except ValueError:
            print(f"Invalid KEY4HEP release argument, YYYY-MM-DD expected, latest possible date {datetime.today().strftime('%Y-%m-%d')}")
            print(f"Requested: {releaseDate}")
            print("Cannot configure scripts correctly, exiting")
            exit()
    else:
        print(f"key4HEP configuration date: latest")
    # store for future use:
    ReleaseSpec.set_info("key4hepReleaseDate",releaseDate)

    # so additionally we read the argument ecmsFile
    for ecmsfile in ecmsfiles:
        # open and read ecms file and append the energies to the command line arguments
        ecmSettings = Settings.ECMSInput(ecmsfile)
        energies.extend(ecmSettings.energies())

    # now we read the global settings
    try:
        # make sure that we follow a symlink to the real location of the parametersets should replace that by share?
        parameterSet = Settings.ParameterSets(paramFileName, paramTag)
    except FileNotFoundError as e:
        print(f"ERROR: File {e} with parameters for tag {paramTag} not found")
        exit()
    
    # now execute file processes
    if len(energies) == 0:
        executeFiles(files, 0, rndmSeed, events)
    else:
        for sqrts in energies:
            rndmIncrement = executeFiles(files, sqrts, rndmSeed, events)
            # offset for next round by number of yaml files
            rndmSeed = rndmSeed + rndmIncrement


def executeFiles(files, sqrts, rndmSeedFallback=4711, events=-1):
    if sqrts == 0:
        print("Generating and writing configuration files")
    else:
        print("Generating and writing configuration files for ECM= ", sqrts)

    for yaml_file in files:
        # read the input file
        settings = Settings.Input(yaml_file, sqrts)
        # ana = analysis.Analysis(settings)
        if settings.rivetON():
            print("Rivet is enabled")
        if settings.key4HEPAnalysisON():
            print("key4HEPAnalysis is enabled")
        if events != -1:
            settings.set("events", events)
        settings.gens()
        processes     = settings.get_processes(sqrts)
        particle_data = settings.get_particle_data()
        generators    = generators_module.Generators(settings)
        try:
            output_dir = getattr(settings, "outdir", "Run-Cards")
        except KeyError:
            # If no directory set in input, use default
            output_dir = "Run-Cards"

        process_instances = {}
        rndmIncrement = 0
        for key, value in processes.items():
            make_output_directory(settings.gens(), output_dir, key)
            try:
                randomseed = value["randomseed"]
            except:
                randomseed = rndmSeedFallback + rndmIncrement
                value["randomseed"] = randomseed
                rndmIncrement += 1
            param = process_module.ProcessParameters(settings)
            process_instances[key] = process_module.Process(
                value, key, param, OutDir=output_dir
            )
            # increment counter for randomseed
        for process_instance in process_instances.values():
            process_instance.prepareProcess(particle_data)
            generators.runGeneratorConfiguration(process_instance)

    return rndmIncrement


if __name__ == "__main__":
    main()
