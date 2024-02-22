import os
import sys
import shutil
import argparse
import textwrap

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'Tools')))
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), 'Generators')))

import Input as Settings
import Particles as particles
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
    #parser = argparse.ArgumentParser(prog='k4gen',description='Process input YAML files.')
    parser = argparse.ArgumentParser(
    prog='k4gen',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
Process input YAML files.
The following options are available:
------------------------------------
SqrtS        : float (center of mass energy)
ISRmode      : int (0: off, 1: on)
OutputFormat : string (format output, available are hepmc and evx)
OutDir       : string (output directory, default=$PWD/Run-Cards)
Events       : unsigned int (Number of Monte-Carlo events to be generated)
Processes    : see README A list of processes which runcards should be generated. Each process should have its own unique name
		Processes:
		  Muon:
		     Initial: [11, -11]
		     Final: [13, -13]
		     Order: [2,0]
RandomSeed   : unsigned int (specify a random seed, important when generating multiple files for the same process)
ParticleData : overwrite basic particle properties
		ParticleData:
		  25:
		    mass: 125
		    width: 0

For MADGRAPH and Whizard only:
ElectronPolarisation : float (between [-1.,1.])
PositronPolarisation : float (between [-1.,1.])
Beamstrahlung        : string (name of accelerator: ILC, FCC, CLIC, C3, HALFHF) 
    '''))
    parser.add_argument('-f', nargs='*', type=str, default=[], help='Input YAML file')
    args = parser.parse_args()
    files = args.f

    for yaml_file in files:
        settings = Settings.Input(yaml_file)
        settings.gens()
        processes = settings.get_processes()
        sqrt_s = settings.get_sqrt_s()
        model = settings.get_model()
        events = settings.get_event_number()
        particle_data = settings.get_particle_data()
        generators = generators_module.Generators(settings)
        try:
          output_dir = getattr(settings, 'outdir', 'Run-Cards')
        except KeyError:
            # If no directory set in input, use default
            output_dir = 'Run-Cards'


        process_instances = {}
        for key, value in processes.items():
            make_output_directory(settings.gens(), output_dir, key)
            initial = value['initial']
            final = value['final']
            order = value['order']
            try:
                decay = value['decay']
            except:
                decay= None
            param = process_module.ProcessParameters(settings)
            process_instances[key] = process_module.Process(initial, final, sqrt_s,
                                                            order, key, decay, param, OutDir=output_dir)

        for process_instance in process_instances.values():
            process_instance.process_info()
            process_instance.set_particle_data(particle_data)
            generators.set_process_info(process_instance)
            generators.initialize_generators()


if __name__ == '__main__':
    main()
