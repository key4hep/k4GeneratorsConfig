#!/usr/bin/env bash

set -e

shopt -s expand_aliases

CWD=${PWD}
# clean up the test directory
rm -r "${CWD}/ci-setups"
exit 0
