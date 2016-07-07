#!/bin/env python3.5
#Author: Saurabh Pathak
#Module for PCA. It takes as argument the database to work on and number of principle
#components to select-- defaults to yalefaces and 150 respectively if not given
#saves the data structures on disk so that recognize module can use it to recognize
from matplotlib import pyplot as pl
from cv2 import resize, cvtColor, COLOR_RGB2GRAY
from numpy import cov, matrix, argsort, save, abs
from numpy.linalg import eig
from os import listdir, makedirs
from sys import argv

l, h, w = len(argv), 50, 50
try:
    database, n = ('yalefaces', 150) if l < 2 else (argv[1], 150) if l == 2 else (argv[1], int(argv[2]))
except:
    print('Improper arguments :(')
    exit(1)

#can work on both color and greyscale datasets
print('Doing PCA on {}...'.format(database), end='', flush=True)
dataset, ordered = [], listdir('../'+ database + '/trainset')
for filename in ordered:
    im = pl.imread('../' + database + '/trainset/' + filename)
    if len(im.shape) > 2 and im.shape[2] == 3:
        im = cvtColor(im, COLOR_RGB2GRAY)
    dataset += resize(im, (h, w)).flatten(),
dataset = matrix(dataset, 'int16')
dmean = dataset.mean(0, 'int16')
dataset -= dmean
e, v = eig(cov(dataset, rowvar=0))
v = v[:, argsort(abs(e))[::-1]][:,:n].real
print('Done. Eigenfaces generated.')

if 'y' in input('Do you want to see a few eigenfaces?(y/n)').lower():
    print('Okay. Showing you 3 most important ones..')
    for i in range(3):
        pl.figure('Eigenface ' + str(i))
        pl.imshow(v[:,i].T.reshape((h,w)), cmap=pl.get_cmap('Greys_r'))
    pl.show()

print('Saving training data to disk...', end='', flush=True)
makedirs('data', exist_ok=True)
save('data/vectors.npy', v)
save('data/dataset.npy', dataset)
save('data/dmean.npy', dmean)
save('data/ordered.npy', ordered)
save('data/resize.npy', (h,w,database))
print('Done. Enjoy recognizing faces!!')
