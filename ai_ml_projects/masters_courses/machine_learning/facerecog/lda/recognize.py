#!/bin/env python3.5
from matplotlib import pyplot as pl
from cv2 import resize, cvtColor, COLOR_RGB2GRAY
from numpy import matrix, argmin, load
from numpy.linalg import norm
from os import listdir

print('Looking for training data on disk...', end='', flush=True)
try:
    ordered, dmean, pf, v, W, (h, w, database) = load('data/ordered.npy'), load('data/dmean.npy'), load('data/trainset.npy'), load('data/pcavectors.npy'), load('data/ldavectors.npy'), load('data/resize.npy')
    print('Found.')
except IOError:
    print('not found.\nWill now generate training data...')
    from train import *

print('Classifier ready. Recognizing testcases...', end='', flush=True)
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
    dists = norm((pf - (matrix(resize(im, tuple(map(int,(h,w)))).flatten(), 'int16') - dmean) * v) * W, axis=1)

    pl.subplot(122)
    pl.title('output')
    pl.axis('off')
    if min(dists) < 2000:
        pl.imshow(pl.imread('../' + database + '/trainset/' + ordered[argmin(dists)]), cmap=pl.get_cmap('Greys_r'))
        pl.show()
    else: print('No match in', database, 'database for', filename, ':(')
print('Done')
