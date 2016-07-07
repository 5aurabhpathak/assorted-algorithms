#!/bin/env python3.5
from matplotlib import pyplot as pl
from cv2 import resize, cvtColor, COLOR_RGB2GRAY
from numpy import cov, matrix, argsort, save, zeros
from numpy.linalg import eig, inv
from os import listdir, makedirs
from sys import argv

l, h, w  = len(argv), 50, 50
try:
    database, t, c, n = ('yalefaces', 7, 15, 100) if l < 2 else (argv[1], 7, 15, 100) if l == 2 else ('yalefaces', int(argv[1]), int(argv[2]), 100) if l == 3 else (argv[1], int(argv[2]), int(argv[3]), 100) if l==4 else (argv[1], int(argv[2]), int(argv[3]), int(argv[4]))
except:
    print('Improper arguments :(')
    exit(1)

print('Doing PCA on data...', end='', flush=True)
dataset, ordered = [], sorted(listdir('../' + database + '/trainset'))
for filename in ordered:
    im = pl.imread('../' + database + '/trainset/' + filename)
    if len(im.shape) > 2 and im.shape[2] == 3:
        im = cvtColor(im, COLOR_RGB2GRAY)
    dataset += resize(im, (h, w)).flatten(),
dataset = matrix(dataset, 'int16')
dmean = dataset.mean(0, 'int16')
dataset -= dmean
e, v = eig(cov(dataset, rowvar=0))
v = v[:, argsort(e)[::-1]][:,:n].real
pf = dataset * v
print('Done. Eigenfaces generated.')

def showfaces(what, vectors, num, h, w):
    if 'y' in input('Do you want to see a few ' + what + '?(y/n)').lower():
        print('Okay. Showing you ' + str(num) + ' most important ones..')
        for i in range(num):
            pl.figure('Eigenface ' + str(i))
            pl.imshow(vectors[:,i].T.reshape((h,w)), cmap=pl.get_cmap('Greys_r'))
        pl.show()

showfaces('Eigenfaces', v, 3, h, w)
print('Doing LDA on reduced data...', end='', flush=True)
M, SW, SB = pf.mean(0), matrix(zeros((n,n))), matrix(zeros((n,n)))
for i in range(0, pf.shape[0], t):
    dataseti = pf[i:i+t]
    mewi = dataseti.mean(0)
    SB += mewi.T * (mewi - M)
    SW += cov(dataseti, rowvar=0)

e, W = eig(inv(SW) * SB)
W = W[:, argsort(e)[::-1]][:,:c - 1].real
print('Done. Fisherfaces generated.')
#showfaces('Fisherfaces', W, 6, 25, 10)

print('Saving training data to disk...', end='', flush=True)
makedirs('data', exist_ok=True)
save('data/pcavectors.npy', v)
save('data/trainset.npy', pf)
save('data/dmean.npy', dmean)
save('data/ordered.npy', ordered)
save('data/ldavectors.npy', W)
save('data/resize.npy', (h,w,database))
print('Done. Enjoy recognizing faces!!')
