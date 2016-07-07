#!/bin/env python3.5
from matplotlib import pyplot as pl
from numpy import argsort, argmin, abs, matrix, ones, square
from numpy.linalg import eig, norm
from cv2 import cvtColor, COLOR_RGB2GRAY
from os import listdir

database = 'yalefaces'
n= 150

def formdataset(directory):
    dataset, order = [], listdir('../' + database + '/' + directory)
    for filename in order:
        im = pl.imread('../' + database + '/' + directory + '/' + filename)
        if len(im.shape) > 2 and im.shape[2] == 3:
            im = cvtColor(im, COLOR_RGB2GRAY)
        dataset += im.flatten(),
    dataset = matrix(dataset, 'float64')
    dmean = dataset.mean(0)
    return dataset - dmean, order

def kernel(x,y):
    K = square(1 + x * y)
    #centering kernel
    onebyn = matrix(ones((K.shape[0], K.shape[0]))) / len(ordered)
    onebyn_1 = matrix(ones((K.shape[1], K.shape[1]))) / len(ordered)
    temp = onebyn * K
    return K - temp  - K * onebyn_1 + temp * onebyn_1

train, ordered = formdataset('trainset')
K = kernel(train, train.T)
e, alpha = eig(K)
alpha = alpha[:, argsort(abs(e))[::-1]][:,:n]
projection = K * alpha

test, ordered_t = formdataset('testset')
K_t = kernel(test, train.T)
projection_t = K_t * alpha

for j, filename in zip(range(test.shape[0]), ordered_t):
    pl.figure(filename)
    pl.subplot(121)
    im = pl.imread('../' + database + '/testset/' + filename)
    if len(im.shape) > 2 and im.shape[2] == 3:
        pl.imshow(im)
        im = cvtColor(im, COLOR_RGB2GRAY)
    else: pl.imshow(im, 'Greys_r')
    pl.title('Input')
    pl.axis('off')
    #calculates distance
    dists = norm(projection - projection_t[j], axis=1)

    pl.subplot(122)
    pl.title('Match')
    pl.axis('off')
    out = pl.imread('../' + database + '/trainset/' + ordered[argmin(dists)])
    if len(im.shape) > 2 and im.shape[2] == 3: pl.imshow(out)
    else: pl.imshow(out, 'Greys_r')
    pl.show()
