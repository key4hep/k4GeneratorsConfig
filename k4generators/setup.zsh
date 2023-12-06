#!/usr/bin/env zsh


# Automatically get the directory where this script is located
K4GenDir=$(cd -- "$(dirname -- "${(%):-%x}")" && pwd)


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

# Set executable
alias k4gen="python3 ${K4GenDir}/python/main.py"
