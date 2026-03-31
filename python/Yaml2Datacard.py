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

def make_output_directory(generators, output_directory, procname):
    # Overwrite directory if it exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for generator in generators:
        generator_directory = os.path.join(output_directory, generator, procname)
        if not os.path.exists(generator_directory):
            os.makedirs(generator_directory)

def Yaml2Datacard(args=None):

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
    energies = []
    if args.sqrts:
        ecmSettings = Reader.SQRTSReader(args.sqrts)
        energies.extend(ecmSettings.energies())

    # now we read the global settings
    try:
        # make sure that we follow a symlink to the real location of the parametersets should replace that by share?
        parameterSet = Reader.ParameterSetReader(args.parameterTagFile, args.parameterTag)
    except FileNotFoundError as e:
        print(f"ERROR: File {e} with parameters for tag {args.parameterTag} not found")
        exit()

    # now execute file processes
    rndmSeed = args.seed
    if len(energies) == 0:
        executeFiles(args.yaml, 0, rndmSeed, args.nevts)
    else:
        for sqrts in energies:
            rndmIncrement = executeFiles(args.yaml, sqrts, rndmSeed, args.nevts)
            # offset for next round by number of yaml files
            rndmSeed = rndmSeed + rndmIncrement

def executeFiles(yaml, sqrts, rndmSeedFallback=4711, events=-1):
    # first step reset all particles:
    ParticleCollection()
    if sqrts == 0:
        print("Generating and writing configuration files")
    else:
        print("Generating and writing configuration files for ECM= ", sqrts)

    # read the input file
    reader = Reader.ProcessReader(yaml, sqrts)
    # set the number of events if present
    if events != -1:
        reader.set("events", events)
    reader.gens()
    processes        = reader.get_processes(sqrts)
    yamlParticleData = reader.get_particle_data()
    generators       = Generators(reader)
    try:
        output_dir = getattr(reader, "outdir", "Run-Cards")
    except KeyError:
        # If no directory set in input, use default
        output_dir = "Run-Cards"

    process_instances = {}
    rndmIncrement = 0
    for key, value in processes.items():
        make_output_directory(reader.gens(), output_dir, key)
        try:
            randomseed = value["randomseed"]
        except:
            randomseed = rndmSeedFallback + rndmIncrement
            value["randomseed"] = randomseed
            rndmIncrement += 1
        param = ProcessParameters(reader)
        # instantiate the class for each process
        process_instances[key] = Process(
            value, key, param, yamlParticleData, OutDir=output_dir
        )
        # increment counter for randomseed
    for process_instance in process_instances.values():
        process_instance.prepareProcess()
        generators.runGeneratorConfiguration(process_instance)

    return rndmIncrement


if __name__ == "__main__":
    Yaml2Datacard()
