#!/bin/bash

set -o errexit
set -o nounset

cat readme_start.md <(echo) <(../splot.py -h | sed 's/^/    /') > ../README.md
