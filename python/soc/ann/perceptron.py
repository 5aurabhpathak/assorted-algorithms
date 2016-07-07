#!/bin/env python3.5
from matplotlib import pyplot as pl
from numpy import matrix, array, sign, nonzero, ones, hstack
from numpy.random import rand

class Perceptron:

    def __init__(self, func):
        self.func = func

    def learn(self, dataset, y, w=None):
        self.w = None
        dataset = hstack((dataset, ones((dataset.shape[0], 1))))
        if not w: w = matrix(rand(dataset.shape[1]))
        diff = self.func(dataset, w) - y.T
        while any(diff):
            n = nonzero(diff)[0][0]
            w = w + y.T[n] * dataset[n]
            diff = self.func(dataset, w) - y.T
        self.w = array(w).flatten()

def step(inputs, w): return sign(inputs * w.T)

def show(s):
    pl.title(s)
    pl.scatter(data[:,0], data[:,1])
    x = pl.gca().get_xlim()
    y = [(- p.w[1] * xi - p.w[2]) / p.w[0] for xi in x]
    pl.plot(x, y, 'r')
    pl.show()

p = Perceptron(step)
data = matrix([[0, 0], [0, 1], [1, 0], [1, 1]])
p.learn(data, matrix([[-1, -1, -1, 1]]))
show('And gate')

p.learn(data, matrix([[-1, 1, 1, 1]]))
show('Or gate')
