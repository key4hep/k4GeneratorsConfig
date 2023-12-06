# k4Generators


## k4Generators


## Description
A python based module for the automatic generation of inputfiles for  Monte-Carlo(MC) generators.

## Requirements
`Python >= 3.7`\
`PyYaml`  

Check your python version
```
python --version
```

you can install pyYaml as user with:
```
pip3 install pyyaml --user
```

## Usage
Once you have written your own inputfile(`input.yaml`), as seen in the [examples](https://gitlab.com/aprice/k4generators/-/tree/main/Examples?ref_type=heads), execute the following:\

`python python/main.py -f input.yaml`

This will create a directory containing the desired runcards. The directory can be set in the inputfile as:\
`OutDir: /path/to/out`
