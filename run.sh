#!/bin/bash -l

GIT_COMMIT=$(git describe --tags --abbrev --dirty)
BIN=$(pwd)/gen-py/dino.py
LOG=/tmp/dino.${GIT_COMMIT}.$(date +%s)

python $BIN 2>&1 | tee $LOG
