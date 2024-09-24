#!/usr/bin/env bash

set -e

CWD=${PWD}
# only create the directory if it does not exist yet
if [[ ! -d ${CWD}/ci-setups ]]; then
   mkdir -p ${CWD}/ci-setups
fi

EXAMPLEDIR="${PWD}/../examples"

# only copy if the file does not exist yet:
for yamlFileWithPath in "$EXAMPLEDIR"/FermionProduction.*yaml; do
   yamlFile="$(basename "$yamlFileWithPath")"
   echo checking for ci-setups/"$yamlFile"
   if [[ ! -f ci-setups/"$yamlFile" ]]; then
      echo copying $yamlFileWithPath to ci-setups
      cp -f "$yamlFileWithPath" ci-setups
   fi
done

exit 0
