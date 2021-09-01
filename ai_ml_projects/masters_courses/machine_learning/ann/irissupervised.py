#!/bin/env python3.5
#Author: Saurabh Pathak
from matplotlib import pyplot as pl
from mpl_toolkits.mplot3d import Axes3D
from numpy import genfromtxt, matrix, zeros, exp, tanh
from ann import ANN

cols = {0, 1, 4}
data = genfromtxt('data/iris.data.train', delimiter=',', converters={4: lambda x: 0. if x == b'Iris-setosa' else 1. if x == b'Iris-versicolor' else 2.}, usecols=cols)
dataset, y = matrix(data[:,:2]), data[:,2]

def bitmapper():
    y_new = matrix(zeros((y.shape[0], 3), 'float64'))
    for i in range(y.size): y_new[i, y[i]] = 1
    return y_new.T

y = bitmapper()
print(y)

#nn = ANN(lambda x: 1 / (1 + exp(-x)), (dataset.shape[1], 4, 5, 4, 3))
nn = ANN(tanh, (dataset.shape[1], 7, 3))
nn.learn(dataset, y)
