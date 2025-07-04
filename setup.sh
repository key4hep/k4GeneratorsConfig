#!/usr/bin/env bash


# Automatically get the directory where this script is located
K4GeneratorsConfigDir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )


if ! command -v python3 >/dev/null 2>&1; then
    echo "Python3 is Required!"
fi


SrcDir=(
	""
	"Generators"
	)

for dir in ${SrcDir[@]}; do
	export PYTHONPATH=${K4GeneratorsConfigDir}/python/${dir}:$PYTHONPATH
done

if [[ ! -d "${K4GeneratorsConfigDir}/install/" ]]; then
    echo Install directory not found!
    echo After:
    echo cmake ../CMakeLists.txt -DCMAKE_INSTALL_PREFIX=../install
    echo Please run:
    echo make install
    exit 1
fi

# Set executable
alias k4GeneratorsConfig="python3 ${K4GeneratorsConfigDir}/python/main.py"
