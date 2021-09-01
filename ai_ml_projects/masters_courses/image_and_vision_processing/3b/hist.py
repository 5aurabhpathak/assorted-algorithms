#!/bin/env python3.5
from matplotlib import pyplot as pl
from numpy import zeros, arange, hstack

def histeq(im):
    hist, intensitymap, histout, out, runningsum = zeros(256), zeros(256, 'uint8'), zeros(256), zeros((im.shape[0], im.shape[1]), 'uint8'), 0
    for i in range(im.shape[0]):
        for j in range(im.shape[1]): hist[im[i,j]] += 1

    lminusonebyn = 255 / im.size
    for i in range(256):
        runningsum += hist[i]
        intensitymap[i] = int(round(lminusonebyn * runningsum))
        histout[intensitymap[i]] += hist[i]

    for i in range(im.shape[0]):
        for j in range(im.shape[1]): out[i,j] = intensitymap[im[i,j]]

    return hist, histout, out, intensitymap

def plothist(hist):
    for i in range(256): pl.plot([i, i], [0, hist[i]], 'r')

def show(n, c, s, h):
    pl.subplot(100+c*10+n)
    pl.title(s)
    if len(h.shape) == 1: plothist(h)
    else:
        pl.axis('off')
        pl.imshow(h, 'Greys_r')

im = pl.imread('data/cameraman.tif')
hist, histout, out, imap = histeq(im)
pl.figure('Histograms1')
show(1, 2, 'Input', hist)
show(2, 2, 'Output', histout)
pl.figure('Image1')
show(1, 2, 'Input', im)
show(2, 2, 'Output', out)
#pl.show()

z, gz, intensitymap, outsp, histout, runsum = hstack((arange(128), 255 - arange(128, 256))), zeros(256), zeros(256), zeros((im.shape[0], im.shape[1]), 'uint8'), zeros(256), 0
pz = z / sum(z)
for i in range(gz.size):
    runsum += pz[i]
    gz[i] = int(round(255 * runsum))

def findsmallesti(gz, s):
    smallest, smallesti = 0, 0
    for i in range(gz.size):
        if smallest <= gz[i] <= s:
            smallest = gz[i]
            smallesti = i
    return smallesti

for i in range(imap.size):
    intensitymap[i] = findsmallesti(gz, imap[i])

for i in range(im.shape[0]):
    for j in range(im.shape[1]): outsp[i,j] = intensitymap[im[i,j]]

for i in range(im.shape[0]):
        for j in range(im.shape[1]): histout[outsp[i,j]] += 1

pl.figure('Histograms2')
show(1, 3, 'Input', hist / im.size)
show(2, 3, 'Desired', pz)
show(3, 3, 'Output', histout / im.size)
pl.figure('Image2')
show(1, 2, 'Input', im)
show(2, 2, 'Output', outsp)
pl.show()
