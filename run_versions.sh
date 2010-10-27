#!/bin/bash -l

TMP=/tmp/dino
REPO=/Users/nico/projects/dev/facebook/dinoisland
N=100

FILE=./run_versions
if [ $# -gt 0 ]; then FILE=$1; fi

for v in $(cat $FILE); do
    rm -rf ${TMP}/${v}
    mkdir -p ${TMP}/${v} && \
    cd ${TMP}/${v} && \
    git clone $REPO && \
    cd dinoisland
    git checkout $v && \
    screen -dmS dino.$(git describe --tags --long --abbrev=4) $REPO/run.zsh $N
done
rm -rf ${TMP}/${v}
