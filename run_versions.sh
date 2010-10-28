#!/bin/bash -l

TMP=/tmp/dino
REPO=~/projects/dev/facebook/dinoisland
N=100

FILE=./run_versions
if [ $# -gt 0 ]; then FILE=$1; fi

for v in $(cat $FILE); do
    rm -rf ${TMP}/${v}

    mkdir -p ${TMP}/${v} && cd ${TMP}/${v}
    if [ $? -ne 0 ]; then
        echo "Can't mkdir or cd to ${TMP}/${v}. Aborting"
        continue
    fi

    git clone $REPO && cd dinoisland
    if [ $? -ne 0 ]; then
        echo "Can't clone and cd to newly created repo for ${TMP}/${v}. Aborting."
        continue
    fi

    git checkout -q $v
    if [ $? -ne 0 ]; then
        echo "Can't checkout request version $v. Aborting."
        continue
    else
        echo "Run for $v starting..."
        screen -dmS dino.$(git describe --tags --long --abbrev=4) $REPO/run.zsh $N
    fi
done
