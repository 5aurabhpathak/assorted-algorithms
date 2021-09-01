#!/bin/env python3.5
#Author: Saurabh Pathak
from matplotlib import pyplot as pl
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.markers import MarkerStyle
from mpl_toolkits.mplot3d import Axes3D
from numpy import genfromtxt, argmin, copy, mean, array
from numpy.random import randint
from numpy.linalg import norm

k = 7
iterations, shift, previouserr = 0, [0]*k, 999999999
dataset = genfromtxt('dataset/2.csv', 'uint64', delimiter=',', usecols=(1, 2, 3))
centroids = copy(dataset[randint(dataset.shape[0], size=k), :]).astype('float64')

while mean(shift) < previouserr and iterations < 100:
    if iterations > 0:
        previouserr = mean(shift)
    clusters, csum, shift  = [[] for _ in range(k)], [[0]*3 for _ in range(k)], [0]*k
    for i in range(dataset.shape[0]):
        c = argmin(norm(centroids - dataset[i], axis=1))
        clusters[c] += dataset[i],
        oldcenter = copy(centroids[c])
        csum[c] +=  dataset[i]
        centroids[c] = csum[c] / len(clusters[c])
        diff = norm(oldcenter - centroids[c])
        shift[c] = diff
    iterations += 1
    #print(mean(shift))

def geticonmap(n):
    cmap = ScalarMappable(Normalize(0, n-1), 'jet')
    markers = MarkerStyle().filled_markers
    def geticon(i): return cmap.to_rgba(i), markers[randint(len(markers))]
    return geticon

ax = pl.subplot(111, projection='3d')
iconmap, i = geticonmap(k), 0
for cluster in clusters:
    cluster = array(cluster)
    icon = iconmap(i)
    ax.scatter(cluster[:,0], cluster[:,1], cluster[:,2], s=50, c=icon[0], depthshade=False, marker=icon[1])
    i += 1

ax.auto_scale_xyz(dataset[:,0], dataset[:,1], dataset[:,2])
pl.title('Clustered data')
pl.show()
