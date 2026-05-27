# Command Line Options

The command line options are specific to the type of execution requested with the exception of:

| **Key** | **Type** | **Default** | **Function** |
| --- | --- | --- | --- |
|  --outputDir          | string           | Run-Cards | OUTPUTDIR |

which is used as the location of the generator datacards and run scripts to be produced and/or to be run.

## Making

The creation of datacards is triggered by `--make`

| **Key** | **Type** | **Default** | **Function** |
| --- | --- | --- | --- |
| --make                | flag             | false   | make the generator datacards from the yaml files |
| --yaml                | (list of) string |  ---    | Path to the YAML input file(s) and/or directory(ies) |
| --nevts               | integer          | -1      | Number of events to generate |
| --seed                | integer          | 4711    | Random number seed |
| --sqrts               | list of floats/filename | ---     | List of center-of-mass energies |
| --parameterTag        | string           | latest  | Name of the parameter tag to use |
| --parameterTagFile    | string           | ---     | Path to a YAML file with parameter sets |
| --key4hepVersion      | string (date)    | ---     | Specific Key4HEP release in YYYY-MM-DD format |
| --key4hepUseNightlies | flag             | false   | Use nightly Key4HEP builds instead of stable releases |

## Comparing

The comparison of datacards is triggered by `--check`

| **Key** | **Type** | **Default** | **Function** |
| --- | --- | --- | --- |
|  --check              | flag             | false   |  check the generator datacards with respect to the reference |
|  --refDir             | string           | k4GeneratorsConfig/test/ref-results | path to the reference files |
| --generator           | string           | All     | generator to be run      |

## Generating

The generation of the events is triggered by `--generate`

| **Key** | **Type** | **Default** | **Function** |
| --- | --- | --- | --- |
| --generate            | flag             | false   | run the event generation |
| --generator           | string           | All     | generator to be run      |

## Summarizing

The generation of the events is triggered by `--summary`

| **Key** | **Type** | **Default** | **Function** |
| --- | --- | --- | --- |
| --summary             | flag             | false   | compare the results of the event generation process by process and produce summary output in outputDir |


## Short cut

The for convenience `--all` triggers `--make --generate --summary`

| **Key** | **Type** | **Default** | **Function** |
| --- | --- | --- | --- |
|  --all                | flag             | false  |  activates `--make --generate --summary` |

