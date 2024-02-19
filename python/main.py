import os
import sys
import shutil
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'Tools')))
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), 'Generators')))

import Input as Settings
import Particles as particles
import Process as process_module
import Generators as generators_module


def make_output_directory(generators, output_directory):
    # Overwrite directory if it exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for generator in generators:
        generator_directory = os.path.join(output_directory, generator)
        if not os.path.exists(generator_directory):
            os.makedirs(generator_directory)


def main():
    parser = argparse.ArgumentParser(description='Process input YAML files.')
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

        make_output_directory(settings.gens(), output_dir)

        process_instances = {}
        for key, value in processes.items():
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
