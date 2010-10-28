#!/bin/zsh

N=1
if [ $# -gt 0 ]; then N=$1; fi

BIN=$(pwd)/gen-py/herb.py
for i in {1..$N}; do $BIN; done
