#!/bin/bash -l

python $(pwd)/gen-py/dino.py 2>&1 | tee /tmp/dino.$(git describe --tags).$(date +%s)
