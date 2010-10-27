#!/bin/bash -l

GIT_COMMIT=$(git describe --tags --long --abbrev=4 --dirty)
BIN=$(pwd)/gen-py/dino.py
LOG=/tmp/dino.${GIT_COMMIT}.$(date +'%Y%m%d_%H%M%S').log

python $BIN 2>&1 | tee $LOG
