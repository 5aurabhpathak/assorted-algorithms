#!/bin/env python3.5
from matplotlib import pyplot as pl
from cv2 import resize
from numpy import cov, matrix, argsort, argmin, zeros
from numpy.linalg import eig, norm, inv
from os import listdir
from sys import argv

if len(argv) < 2:
    print('Nothing to recognize :(')
    exit(1)

h, w, n, l, dataset, ordered = 50, 50, 100, 50, [], sorted(listdir('../yalefaces/trainset'))
for filename in ordered: dataset += resize(pl.imread('../yalefaces/trainset/' + filename), (h, w)).flatten(),
dataset = matrix(dataset, 'int16')
dmean = dataset.mean(0, 'int16')
dataset -= dmean
e, v = eig(cov(dataset, rowvar=0))
v = v[:, argsort(e)[::-1]][:,:n].real
pf = dataset * v
print('PCA Done..')

M, SW, SB = pf.mean(0), matrix(zeros((n,n))), matrix(zeros((n,n)))
for i in range(0, pf.shape[0], 7):
    dataseti = pf[i:i+7]
    mewi = dataseti.mean(0)
    SB += mewi.T * (mewi - M)
    SW += cov(dataseti, rowvar=0)

e, W = eig(inv(SW) * SB)
print('LDA Done..')
dists = norm((pf - (matrix(resize(pl.imread(argv[1]), (h,w)).flatten(), 'int16') - dmean) * v) * W[:, argsort(e)[::-1]][:,:l].real, axis=1)

if min(dists) < 2000:
    pl.imshow(pl.imread('../yalefaces/trainset/' +ordered[argmin(dists)]), cmap=pl.get_cmap('Greys_r'))
    pl.title('Person in input is same as this person.')
    pl.show()
else: print('No match in database. :(')
