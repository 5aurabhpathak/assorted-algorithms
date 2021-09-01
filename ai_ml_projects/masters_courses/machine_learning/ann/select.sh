#!/bin/bash
#train:test = 40:60
n=$(echo "0.75*$(cat $1 | wc -l)/1" | bc)
shuf $1 | tee >(head -n $n > data/$1.train) | tail -n +$(($n+1)) > data/$1.test
echo successfully created random training set and test set!
