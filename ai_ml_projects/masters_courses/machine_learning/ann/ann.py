#!/bin/env python3.5
#Author: Saurabh Pathak
from matplotlib import pyplot as pl
from numpy import matrix, nonzero, tanh, ones, hstack, sum, square, exp, min, max, abs
from numpy.random import rand
from scipy.misc import derivative

class Perceptron:

    def __init__(self, func, inputs):
        self.func = func
        self.numinputs = inputs
        self.w = matrix(rand(inputs+1))

    def compute(self, inputs):
        self.s = hstack((inputs, ones((inputs.shape[0], 1)))) * self.w.T
        self.out = self.func(self.s)
        return self.out

    def calcdelta(self, n, *param):
        dydx = derivative(self.func, self.s[n], 0.01).A1
        if len(param) == 1: self.delta = dydx * param[0][n].A1
        else: self.delta = dydx * sum(param[0].A * param[1].A)
        return self.delta

    def update(self, xlminus1):
        xlminus1 = hstack((xlminus1, ones((1,1))))
        self.w -= .1 * self.delta * xlminus1

    def plot_decision_boundary(self, xlim):
        w = self.w.A1
        y = [(- w[1] * xi - w[2]) / w[0] for xi in xlim]
        pl.plot(xlim, y, 'r')


class Layer:

    def __init__(self, n, func, numinputs):
        self.numneurons = n
        self.func = func
        self.neurons = [Perceptron(func[i], numinputs) for i in range(n)] if type(func) is list else [Perceptron(func, numinputs) for i in range(n)]

    def compute(self, inputs):
        out, w = [], []
        for n in self.neurons:
            out += n.compute(inputs).A1,
            w += n.w.A1,
        self.out, self.w = matrix(out).T, matrix(w).T
        return self.out

    def calcdeltas(self, n, param):
        deltas, i = [], 0
        for N in self.neurons:
            if isinstance(param, matrix): deltas += N.calcdelta(n, param[:,i]),
            else: deltas += N.calcdelta(n, param.deltas, param.w[i,:]),
            i += 1
        self.deltas = matrix(deltas)
    
    def update(self, n, inputs):
        for N in self.neurons: N.update(inputs[n]),
        return self.out

    def plot_decision_boundaries(self, x):
        for N in self.neurons: N.plot_decision_boundary(x)

class ANN:

    def __init__(self, func, neuronsarray):
        self.n, self.func, self.topology = len(neuronsarray), func, neuronsarray
        self.layers = [Layer(neuronsarray[i], func[i], neuronsarray[i-1]) for i in range(1, self.n)] if type(func) is list else [Layer(neuronsarray[i], func, neuronsarray[i-1]) for i in range(1, self.n)]

    def compute(self, inputs):
        for l in self.layers: inputs = l.compute(inputs)
        self.out = inputs

    def learn(self, data, y):
        self.compute(data)
        diff, self.y = y.T - self.out, y
        e, pe = sum(square(diff)), 0

        while e > .01:
            print(e)
            for n in range(diff.shape[0]):
                self.layers[-1].calcdeltas(n, diff)
                rev = self.layers[::-1]

                #backpropagation
                for i in range(1, len(rev)): rev[i].calcdeltas(n, rev[i-1])

                inputs = data
                for l in self.layers: inputs = l.update(n, inputs)

            self.compute(data)
            diff, pe = self.out -  y.T, e
            e = sum(square(diff))

        print('\n\nActual outputs:', self.out)

    def plot_decision_boundaries(self):
        x = pl.gca().get_xlim()
        for l in self.layers: l.plot_decision_boundaries(x)

    def classify(self, test):
        self.compute(test)
        max_labels, min_labels = max(self.y, 1).A, min(self.y, 1).A
        thresh = min_labels + abs(max_labels - min_labels) / 2
        return (self.out.A > thresh) * max_labels + (self.out.A < thresh) * min_labels

if __name__=='__main__':
    data = matrix([[0, 0], [0, 1], [1, 0], [1, 1]])
    nn = ANN(tanh, (2, 5, 1))
    nn.learn(data, matrix([[-1, 1, 1, -1]]))
    pl.title('Xor gate')
    pl.scatter(data[(1,2),0], data[(1,2),1], c='r')
    pl.scatter(data[(0,3),0], data[(0,3),1], c='b')
    #nn.plot_decision_boundaries() #linear boundary approximations from each neauron

    test = matrix(rand(100,2))
    labels = nn.classify(test)
    for i in range(test.shape[0]):
        if labels[i,0] == -1: pl.scatter(test[i,0], test[i,1], c='b')
        else: pl.scatter(test[i,0], test[i,1], c='r')
    pl.show()
