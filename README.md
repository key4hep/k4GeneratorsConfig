# k4Generators


## k4Generators


## Description
A python based module for the automatic generation of inputfiles for  Monte-Carlo(MC) generators.


## Prerequisits

Check your python version
```
python --version
```
The package needs at least python v3.7. 

yaml should be available, if not, you can install as user with:
```
pip3 install pyyaml --user
```

## Usage
Once you have written your own inputfile(`input.yaml`), as seen in the [examples](https://gitlab.com/aprice/k4generators/-/tree/main/Examples?ref_type=heads), execute the following:\

`python python/main.py -f input.yaml`

This will create a directory containing the desired runcards. The directory can be set in the inputfile as:\
`OutDir: /path/to/out`
