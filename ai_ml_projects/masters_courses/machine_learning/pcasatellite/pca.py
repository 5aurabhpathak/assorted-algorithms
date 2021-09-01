#!/bin/env python3.5
#Author: Saurabh Pathak
from matplotlib import pyplot as pl
from numpy import cov, dstack, matrix, argsort, abs
from numpy.linalg import eig
from cv2 import equalizeHist

#[:,:,0] since imread in pyplot reads four channels from even a single channel gif. This is a bug in pyplot and [:,:,0] is a workaround until they fix it.
im = matrix(dstack((pl.imread('../bayesian/1.gif',)[:,:,0], pl.imread('../bayesian/2.gif')[:,:,0], pl.imread('../bayesian/3.gif')[:,:,0], pl.imread('../bayesian/4.gif')[:,:,0])).reshape((512*512, 4)))
e, v = eig(cov(im, rowvar=0))
im = (im * v[:, argsort(abs(e))]).astype('uint8')
for i in range(4):
    pl.figure('Principal Component ' + str(i+1))
    pl.imshow(equalizeHist(im[:,i].reshape((512, 512))), pl.get_cmap('Greys_r'))
    pl.axis('off')
pl.show()
