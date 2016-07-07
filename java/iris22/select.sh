#!/bin/bash
shuf $1 | tee >(head -n 30 > data/IRIS.train) | tail -n +31 > data/IRIS.test
echo successfully created random training set
