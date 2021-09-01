#/bin/env python3.5
from matplotlib import pyplot as pl
from numpy import matrix, vsplit, hsplit

c = pl.imread('data/cameraman.tif')
c1, c2 = vsplit(c, 2)
(c11, c12), (c21, c22) = hsplit(c1, 2), hsplit(c2, 2)

def subpl(im, subfig):
    pl.subplot(220 + subfig)
    pl.axis('off')
    pl.imshow(im, cmap=pl.get_cmap('Greys_r'), interpolation='none')

subpl(c11, 1)
subpl(c12, 2)
subpl(c21, 3)
subpl(c22, 4)

pl.figure()
subpl(c22, 1)
subpl(c21, 2)
subpl(c12, 3)
subpl(c11, 4)

pl.show()
