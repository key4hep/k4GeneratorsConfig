#!/usr/bin/env bash


# Automatically get the directory where this script is located
K4GenDir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )


if ! command -v python3 >/dev/null 2>&1; then
    echo "Python3 is Required!"
fi


SrcDir=(
	""
	"Generators"
	)

for dir in ${SrcDir[@]}; do
	export PYTHONPATH=${K4GenDir}/python/${dir}:$PYTHONPATH
done

export K4GenBuildDir=${K4GenDir}/build/

if [[ ! -d ${K4GenBuildDir} ]]; then
	echo "Build directory not found! "
	exit 1
fi

# Set executable
alias k4GeneratorsConfig="python3 ${K4GenDir}/python/main.py"
