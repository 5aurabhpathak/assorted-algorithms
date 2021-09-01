#!/bin/env python3.5
#Author: Saurabh Pathak (phoenix)
import matplotlib.pyplot as pl, sys, math as m
from decimal import Decimal
from numpy import *
from numpy.linalg import inv,det

tSRiver = tSLand = None

class Sampler:
    '''handles sampling and contains the mouse click handler'''

    def __init__(self, maxcount):
        self._samples = [[0]*4]
        self.maxcount = maxcount
        self.handle = pl.gcf().canvas.mpl_connect('button_press_event', self)

    def __len__(self): return len(self.samples)

    @property
    def samples(self): 
        if len(self._samples) <= self.maxcount: return self._samples[1:]
        else: return self._samples[1:self.maxcount + 1] #discard if extra

    def __call__(self, event):
        '''click in images to collect samples. samples 9 neighbors in and around the clicked pixel on each click.'''
        x, y = int(event.xdata), int(event.ydata)
        xmin = x - 1 if 0 < x else x
        xmax = x + 2 if x < 511 else x
        ymin = y - 1 if 0 < y else y
        ymax = y + 2 if y < 511 else y
        self._samples = append(self._samples, im[xmin:xmax, ymin:ymax].reshape(abs(xmin-xmax) * abs(ymin-ymax), 4), 0)
        pl.title('{} pixels sampled...'.format(len(self)))
        if len(self) == self.maxcount:
            pl.title('Done! Please close the window.')
            pl.gcf().canvas.mpl_disconnect(self.handle)
        pl.draw()

def trainSetAccumulate():
    global tSRiver, tSLand, im1
    displayim(im4, 'Select 50 river samples: Click 6 places', 'Select from RGBI')
    tSRiver = collectSamples(50)
    displayim(im4, 'Select 100 non river samples.', 'Select from RGBI')
    tSLand = collectSamples(100)

def collectSamples(size):
    s = Sampler(size)
    pl.show()
    return s.samples

def naiveBayes():
    global tSRiver, tSLand, im, outimg
    covRiver, covLand = cov(tSRiver, rowvar=0), cov(tSLand, rowvar=0)
    icr, icl= inv(covRiver), inv(covLand)
    meanRiver, meanLand = mean(tSRiver, axis=0), mean(tSLand, axis=0)

    for i in range(512):
        for j in range(512):
            devRiver, devLand = subtract(im[i,j], meanRiver), subtract(im[i,j], meanLand)
            rivClass = dot(dot(devRiver, icr), devRiver.T)
            nrivClass = dot(dot(devLand, icl), devLand.T)

            try:
                p1 = Decimal(-0.5)/Decimal(m.sqrt(det(covRiver))) * Decimal(m.exp(rivClass))
            except OverflowError:
                outimg[i,j] = 255
                continue# as e: print(e, 'Variable in exp: ', rivClass)
            try:
                p2 = Decimal(-0.5)/Decimal(m.sqrt(det(covLand))) * Decimal(m.exp(nrivClass))
            except OverflowError: continue# as e:
#                print(e, 'Variable in exp: ', rivClass, ' Setting pixel to 0')
            class1 = Decimal(P1)*p1
            class2 = Decimal(P2)*p2

            if class1 >= class2: outimg[i,j] = 255

def displayim(img, prompt, title):
    pl.imshow(img, origin='upper')
    pl.title(prompt)
    pl.gcf().canvas.set_window_title(title)
    pl.xlim(0,512)
    pl.ylim(512,0)

def printUsage():
    print('Usage: bayesian.py P1 P2')
    quit(1)

im1 = pl.imread('data/1.gif')[:,:,0]
im2 = pl.imread('data/2.gif')[:,:,0]
im3 = pl.imread('data/3.gif')[:,:,0]
im4 = pl.imread('data/4.gif')
im = dstack((im1,im2,im3,im4[:,:,0]))
P1, P2 = None, None
if len(sys.argv) != 3: printUsage()
P1, P2 = sys.argv[1], sys.argv[2]

outimg = zeros((512, 512, 3), dtype='bool')
trainSetAccumulate()
print('Working...', end='', flush=True)
naiveBayes()
print('done.')
displayim(outimg, 'P(river): '+str(P1)+'     P(Non-river): '+str(P2), 'Naive Bayes Output')
pl.show()
