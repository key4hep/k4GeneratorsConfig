#!/bin/bash

# Automatically get the directory where this script is located
K4GenDir=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" && pwd )

SrcDir=(
	"src"
	"tools"
	"Generators"
	)

for dir in ${SrcDir[@]}; do
	export PYTHONPATH=${K4GenDir}/${dir}:$PYTHONPATH
done

# Set executable
alias k4gen="python ${K4GenDir}/src/main.py"