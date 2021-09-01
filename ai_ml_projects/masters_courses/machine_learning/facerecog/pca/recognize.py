#!/bin/env python3.5
#Recognizer module-- call it after train.py
#reads trained data structures on disk and recognizes the corresponding dataset's testset folder for which it has been trained
#if no data is found on disk, it calls train.py with default arguments (yalefaces, 150) and proceeds to recognize its testset folder
#can handle both color and greyscale input
from matplotlib import pyplot as pl
from cv2 import resize, cvtColor, COLOR_RGB2GRAY
from numpy import matrix, argmin, load
from numpy.linalg import norm
from os import listdir

print('Looking for training data on disk...', end='', flush=True)
try:
    ordered, dmean, dataset, v, (h, w, database) = load('data/ordered.npy'), load('data/dmean.npy'), load('data/dataset.npy'), load('data/vectors.npy'), load('data/resize.npy')
    print('Found.')
except IOError:
    print('not found.\nWill now generate training data using default dataset...')
    from train import *

print('Classifier ready. Recognizing testcases...', end='', flush=True)
i = 0
for filename in listdir('../' + database + '/testset'):
    pl.figure(filename)
    pl.subplot(121)
    im = pl.imread('../' + database + '/testset/' + filename)
    if len(im.shape) > 2 and im.shape[2] == 3:
        pl.imshow(im)
        im = cvtColor(im, COLOR_RGB2GRAY)
    else: pl.imshow(im, cmap=pl.get_cmap('Greys_r'))
    pl.title('Input')
    pl.axis('off')
#calculates distance
    dists = norm((dataset - (matrix(resize(im, tuple(map(int,(h,w)))).flatten(), 'int16') - dmean)) * v, axis=1)

    pl.subplot(122)
    pl.title('Match')
    pl.axis('off')
    if min(dists) < 3000:
        out = pl.imread('../' + database + '/trainset/' + ordered[argmin(dists)])
        if len(im.shape) > 2 and im.shape[2] == 3: pl.imshow(out)
        else: pl.imshow(out, cmap=pl.get_cmap('Greys_r'))
        pl.show()
    else: print('No match in', database, 'database for', filename, ':(')
    i += 1
    if i > 9:
        i = 0
        if 'n' in input('Do you want to continue?(y/n)').lower(): break

print('Done')
