Command Line Options
=====================================

| **Key** | **Type** | **Default** | **Function** |
| --- | --- | --- | --- |
| (positional)          | string           |  ---    | Path to the YAML input file |
| --nevts               | integer          | -1      | Number of events to generate |
| --seed                | integer          | 4711    | Random number seed |
| --ecms                | list of floats   | ---     | List of center-of-mass energies |
| --ecmsFiles           | list of strings  | ---     | List of YAML files specifying energy points |
| --parameterTag        | string           | latest  | Name of the parameter tag to use |
| --parameterTagFile    | string           | ---     | Path to a YAML file with parameter sets |
| --key4hepVersion      | string (date)    | ---     | Specific Key4HEP release in YYYY-MM-DD format |
| --key4hepUseNightlies | flag             | false   | Use nightly Key4HEP builds instead of stable releases |
