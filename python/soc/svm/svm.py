#!/bin/env python3.5
#Author: Saurabh Pathak
from matplotlib import pyplot as pl, patches
from mpl_toolkits.mplot3d import Axes3D
from numpy import genfromtxt, multiply, ones, zeros, identity, around, meshgrid, amin, argsort, vstack, matrix as mat, array, hstack
from numpy.random import random_integers
from scipy.spatial.distance import cdist, pdist, squareform
from cvxopt.solvers import qp, options
from cvxopt import matrix

cols, condition, s_size, test = {0, 1, 2, 4}, b'Iris-setosa', 3, False
data = genfromtxt('data/iris.data.train', delimiter=',', converters={4: lambda x: 1.0 if x == condition else -1.0}, usecols=cols)
dataset_primal, y_primal = data[:,:3], data[:,3]

#training data selection - begin
def selectfromtrainset(s):
    dataset_1, dataset_2, y1, y2 = [], [], [], []
    for i in range(dataset_primal.shape[0]):
        if y_primal[i] == -1:
            dataset_1 += dataset_primal[i],
            y1 += y_primal[i],
        else:
            dataset_2 += dataset_primal[i],
            y2 += y_primal[i],
    dataset_1, dataset_2, y1, y2 = mat(dataset_1), mat(dataset_2), array(y1), array(y2)

    def choosemetric():
        crossdist = cdist(dataset_1, dataset_2, 'euclidean')
        m_1, m_2 = amin(crossdist, 1), amin(crossdist, 0)
        s1, s2 = 2 * s_size // 3, s_size // 3
        if s == 'hausdorff': samples_1, samples_2 = argsort(m_1)[:s1], argsort(m_2)[:s2]
        if s == 'confidence':
            withindist_1, withindist_2 = squareform(pdist(dataset_1, 'euclidean')), squareform(pdist(dataset_2, 'cityblock'))

            def radius(w, m):
                ni = zeros(w.shape[0])
                for i in range(w.shape[0]):
                    for j in range(w.shape[1]):
                        if w[i,j] > ni[i] and w[i,j] < m[i]: ni[i] = w[i,j]
                return ni

            ni_1, ni_2 = radius(withindist_1, m_1), radius(withindist_2, m_2)
            samples_1, samples_2 = argsort(ni_1)[:s1], argsort(ni_2)[:s2]
        elif s == 'random': samples_1, samples_2 = random_integers(0, dataset_1.shape[0] - 1, s1), random_integers(0, dataset_2.shape[0] - 1, s2)
        return dataset_1[samples_1], dataset_2[samples_2], y1[samples_1], y2[samples_2]

    dataset_1, dataset_2, y1, y2  = choosemetric()
    return matrix(vstack((dataset_1, dataset_2))), matrix(hstack((y1, y2)))

def plotsurface(w, b, maxrange, ax, color):
    surface_x, surface_y = meshgrid(range(maxrange), range(maxrange))
    surface_z = (-w[0] * surface_x - w[1] * surface_y - b) / w[2]
    ax.plot_surface(surface_x, surface_y, surface_z, color=color, alpha=0.5)
    

def applysvm(selection_metric, test):
    if selection_metric == 'none': dataset, y = matrix(dataset_primal), matrix(y_primal)
    else: dataset, y = selectfromtrainset(selection_metric)

    innerproducts = matrix(multiply(y * y.T, dataset * dataset.T))
    options['show_progress'] = False
    solution = qp(innerproducts, matrix(-ones(dataset.size[0])), matrix(-identity(dataset.size[0])), matrix(zeros(dataset.size[0])), y.T, matrix(0.0))
    alpha = matrix(around(solution['x'], 5))

    params = [(alpha[i], y[i], dataset[i,:]) for i in range(dataset.size[0]) if alpha[i] != 0.0]
    w = sum([params[i][0] * params[i][1] * params[i][2] for i in range(len(params))])
    b = 1 / params[0][1] - w * params[0][2].T

    #training complete. Rest is plotting and test
    maxrange = None
    def plot(ax, s):
        nonlocal maxrange
        for i in range(dataset.size[0]):
            if y[i] == -1:
                if alpha[i] == 0.0: ax.scatter(dataset[i, 0], dataset[i,1], dataset[i,2], s=30, c='b')
                else: ax.scatter(dataset[i, 0], dataset[i,1], dataset[i,2], s=40, c='b', marker='D')
            else:
                if alpha[i] == 0.0: ax.scatter(dataset[i, 0], dataset[i,1], dataset[i,2], s=30, c='r')
                else: ax.scatter(dataset[i, 0], dataset[i,1], dataset[i,2], s=40, c='r', marker='D')

        pl.title('Linear SVM - Hard Margin - ' + s)
        maxrange = int(max(dataset[:,:2])) + 1
        plotsurface(w, b, maxrange, ax, 'g')

    if not test:
        pl.figure('Using selection method: ' + selection_metric)
        ax = pl.subplot(111, projection='3d')
        plot(ax, 'Train')
        return w, b, maxrange

    #begin testing
    pl.figure('Using selection method: ' + selection_metric)
    ax = pl.subplot(111, projection='3d')
    data = genfromtxt('data/iris.data.test', delimiter=',', converters={4: lambda x: 1.0 if x == condition else -1.0}, usecols=cols)
    testset, y_actual= matrix(data[:,:3]), matrix(data[:,3])
    y_obs, numerrors = zeros(testset.size[0]), 0
    for i in range(testset.size[0]):
        y_obs[i] = 1 if (w * testset[i,:].T + b)[0] > 0.0 else -1
        if y_actual[i] != y_obs[i]: numerrors += 1
        if y_actual[i] == -1: ax.scatter(testset[i,0], testset[i,1], testset[i,2], c='aqua')
        else: ax.scatter(testset[i,0], testset[i,1], testset[i,2], c='plum')
    plot(ax, 'Test')
    print('% Error using {}:'.format(selection_metric), 100.0 * numerrors / testset.size[0])
    return w, b, maxrange

pl.figure('Comparison')
handles = []
ax = pl.subplot(111, projection='3d')

def compare(t, c):
    global handles
    plotsurface(*applysvm(t, test), ax, c)
    handles += patches.Patch(color=c, label=t),

compare('none', 'r')
compare('hausdorff', 'g')
compare('confidence', 'b')
compare('random', 'y')
pl.figure('Comparison')
pl.figlegend(handles, ('none', 'hausdorff', 'confidence', 'random'), 'upper right')
pl.show()
