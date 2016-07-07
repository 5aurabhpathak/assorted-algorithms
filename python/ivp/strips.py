#!/bin/env python3.5
from matplotlib import pyplot as pl
from numpy import matrix, zeros, vstack, hstack

ima = matrix(zeros((16,16)), bool)
for i in range(ima.shape[0]):
    for j in range(0, ima.shape[1], 2): ima[i, j] = True

pl.figimage(ima, cmap=pl.get_cmap('binary_r'), xo=250, yo=250)
pl.imsave('data/16x16strip.jpg', ima, cmap=pl.get_cmap('binary_r'))

imb = matrix(zeros((16,16)), bool)
for i in range(0, imb.shape[0], 2):
    for j in range(0, imb.shape[1], 2): imb[i, j] = True

pl.figimage(imb, cmap=pl.get_cmap('binary_r'), xo=270, yo=270)
pl.imsave('data/chequred16x16.jpg', imb, cmap=pl.get_cmap('binary_r'))

x, y = vstack((ima, ima, imb, imb)), vstack((imb, imb, ima, ima))
imc = hstack((x, x, y, y))
pl.figimage(imc, cmap=pl.get_cmap('binary_r'), xo=300, yo=270)
pl.imsave('data/combined.jpg', imc, cmap=pl.get_cmap('binary_r'))
pl.show()
