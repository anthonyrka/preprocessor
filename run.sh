#!/usr/bin/env bash
IFILE = $1
P = $2

time python preprocess.py $1 $2
time python featurizer.py
time python learner.py 40

