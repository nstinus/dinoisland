#!/bin/zsh

N=1
if [ $# -gt 0 ]; then N=$1; fi

GIT_COMMIT=$(git describe --tags --long --abbrev=4 --dirty)
BIN=$(pwd)/gen-py/dino.py

for i in {1..$N}
do
    LOG=/tmp/dino.${GIT_COMMIT}.$(date +'%Y%m%d_%H%M%S').log
    python $BIN 2>&1 | tee $LOG
done
