#!/bin/env python3.5
#Author: Saurabh Pathak
from matplotlib import pyplot as pl
from cv2 import cvtColor, COLOR_RGB2GRAY
from numpy import cov, matrix, argsort, abs, around
from numpy.linalg import eig
from sys import argv

n = 30 if len(argv) == 1 else int(argv[1])
dataset = matrix(cvtColor(pl.imread('me.jpg'), COLOR_RGB2GRAY), 'float64')
if (n > dataset.shape[1]):
    print('Wrong parameter.')
    exit(1)
e, v = eig(cov(dataset, rowvar=0))
v =  v[:, argsort(abs(e))[::-1]][:,:n]

def disp(n, string, im):
    pl.subplot(120 + n)
    pl.title(string)
    pl.imshow(im, 'Greys_r')
    pl.axis('off')

disp(1, 'Input', dataset)
reduced = around(dataset * v * v.T).astype('uint8')
disp(2, 'Output with '+str(n)+' Principal components', reduced)
pl.show()
