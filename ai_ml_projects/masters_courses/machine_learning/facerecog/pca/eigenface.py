#!/bin/env python3.5
#Author: Saurabh Pathak
#File for training and recognizing
#It follows the entire procedure for PCA on each run. Takes one argument -- the image file to recognize. Works on yalefaces databse
from matplotlib import pyplot as pl
from cv2 import resize
from numpy import cov, matrix, argsort, argmin, abs
from numpy.linalg import eig, norm
from os import listdir
from sys import argv

if len(argv) < 2:
    print('Nothing to recognize :(')
    exit(1)

#h= height
#w = width
#images need to be resized to w x h to avoid memory error.
h, w, n, dataset, ordered = 50, 50, 150, [], listdir('../yalefaces/trainset')
for filename in ordered:
    im = pl.imread('../yalefaces/trainset/' + filename)
    if len(im.shape) > 2 and im.shape[2] == 3:
        im = cvtColor(im, COLOR_RGB2GRAY)
    dataset += resize(im, (h, w)).flatten(),
dataset = matrix(dataset, 'int16')
dmean = dataset.mean(0, 'int16')
dataset -= dmean
e, v = eig(cov(dataset, rowvar=0))

im = pl.imread(argv[1])
pl.subplot(121)
pl.title('Input')
pl.axis('off')
if len(im.shape) > 2 and im.shape[2] == 3:
    pl.imshow(im)
    im = cvtColor(im, COLOR_RGB2GRAY)
else: pl.imshow(im, cmap=pl.get_cmap('Greys_r'))
#calculates euclidean distance
dists = norm((dataset - (matrix(resize(im, (h,w)).flatten(), 'int16') - dmean)) * v[:, argsort(abs(e))[::-1]][:,:n].real, axis=1)

if min(dists) < 2000: #threshold
    pl.subplot(122)
    pl.axis('off')
    pl.imshow(pl.imread('../yalefaces/trainset/' +ordered[argmin(dists)]), cmap=pl.get_cmap('Greys_r'))
    pl.title('Match')
    pl.show()
else: print('No match in database. :(')
