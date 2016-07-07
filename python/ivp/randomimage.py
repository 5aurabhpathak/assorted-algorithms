#!/bin/env python 3.5
from matplotlib import pyplot as pl
from cv2 import resize, INTER_LANCZOS4
from numpy import random, zeros

A = random.random_integers(0, 255, (512,512)).astype('uint8')
pl.imshow(A, pl.get_cmap('Greys_r'))
pl.show()

def resizeto(A, res):
    pl.figure(str(res[0]) + 'x' + str(res[1]))
    pl.imshow(resize(A, res, interpolation=INTER_LANCZOS4), pl.get_cmap('Greys_r'))

resizeto(A, (100, 120))
resizeto(A, (600, 512))
resizeto(A, (1024, 1024))
pl.show()

def crop(A, s, c):
    output = zeros(s, 'uint8')
    for i in range(output.shape[0]):
        for j in range(output.shape[1]): output[i,j] = A[c[0] - output.shape[0]/2 + i, c[1] - output.shape[1]/2 + j]
    return output

pl.imshow(crop(A, (300, 300), (A.shape[0]/2, A.shape[1]/2)), pl.get_cmap('Greys_r'))
pl.show()

print('The intensity value at coordinate 100x100 is {}.'.format(A[100,100]))
