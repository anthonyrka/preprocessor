#!/bin/bash
I=$1
O=$2
P=$3

awk -v PROB="$P" 'BEGIN {srand()} !/^$/ { if (rand() <= PROB || FNR==1) print $0}' $I > $O

