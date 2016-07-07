#!/bin/env python3.5
from matplotlib import pyplot as pl
from numpy import max, min

def disp(im, n, t):
    pl.subplot(120 + n)
    pl.title(t)
    pl.axis('off')
    pl.imshow(im, pl.get_cmap('Greys_r'))

im = pl.imread('data/cameraman.tif').astype('uint16')
print('In=\n',im)
disp(im,1, 'input')

out = (30 + im * 150/(max(im) - min(im))).astype('uint8')
print('out=\n', out,'\nMaximum intensity',max(out),'\nMinimum intensity', min(out))
disp(out,2,'output')
pl.show()
