#!/bin/env python3.5
from matplotlib import pyplot as pl
from sklearn.datasets import make_circles
from scipy.spatial.distance import pdist, squareform
from numpy import exp, argsort, abs, zeros, hstack, asmatrix
from numpy.linalg import eig

x, y = make_circles(500, noise=.05, factor=.6)

def plot(x_mat, y_labels, caption):
    for i in range(y_labels.shape[0]):
        if y_labels[i] == 1: pl.scatter(x_mat[i,0], x_mat[i,1], c='b')
        else: pl.scatter(x_mat[i,0], x_mat[i,1], c='r')
    pl.title(caption)
    pl.show()

plot(x, y, 'Original samples')

#the samples generated already centered so no need for centering them
K = asmatrix(exp(squareform(pdist(x, 'sqeuclidean'))))
e, alpha = eig(K)
alpha = alpha[:, argsort(abs(e))[::-1]]
pc = (K * alpha[:,:2]).real
plot(hstack((pc[:,0], zeros((pc.shape[0],1)))), y, 'Principal Component')
plot(pc, y, 'Two Principal Components')
