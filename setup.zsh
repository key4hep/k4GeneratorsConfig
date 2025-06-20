#!/usr/bin/env zsh


# Automatically get the directory where this script is located
K4GeneratorsConfigDir=$(cd -- "$(dirname -- "${(%):-%x}")" && pwd)


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

K4GeneratorsConfigLocalBuildDir=${K4GeneratorsConfigDir}/build/

if [[ ! -d ${K4GeneratorsConfigLocalBuildDir} ]]; then
	echo "Build directory not found! "
	exit 1
fi

export K4GeneratorsConfigBinDir=${K4GeneratorsConfigLocalBuildDir}/bin/

# Set executable
alias k4GeneratorsConfig="python3 ${K4GeneratorsConfigDir}/python/main.py"
