#!/usr/bin/env bash

set -e

mkdir -p test/ref-results
mkdir -p test/ci-setups

tar xf main-res.tar.gz --directory="${PWD}/test/ref-results"
CWD=${PWD}
REFDIR="${PWD}/test/ref-results"
EXAMPLEDIR="${PWD}/../examples"

cd test
cp $EXAMPLEDIR/*yaml ci-setups
cd ci-setups

function checkOutputs() {
    # TODO: Make this nicer than nested loops
    for outerDir in *; do
        if [[ -d "$outerDir" ]]; then
            for generator in "$outerDir"/*; do
                if [[ -d "$generator" ]]; then
                    # echo "Checking $generator"
                    for outFile in $(ls "$PWD/$generator/"); do
                        if [[ -e "$REFDIR/$generator/$outFile" ]]; then
                            echo "Found $outFile in reference results."
                            if diff "$REFDIR/$generator/$outFile" "$PWD/$generator/$outFile" &> /dev/null; then
                                echo "Files are identical."
                            else
                                echo "Files are different."
				diff "$REFDIR/$generator/$outFile" "$PWD/$generator/$outFile"
                                exit 1
                            fi
                        else
                            echo "Did not find $outFile in reference results. Not checking!"
                        fi
                    done
                fi
            done
        fi
    done
}

for yamlFile in *.yaml; do
    # Extract file name without extension
    filename="${yamlFile%.yaml}"
    mkdir -p "test-$filename"
    cd "test-$filename"
    echo "Processing file: $yamlFile"
    python3 ../../../../python/main.py -f "../$yamlFile"
    checkOutputs
done

rm -r ${CWD}/test
exit 0
