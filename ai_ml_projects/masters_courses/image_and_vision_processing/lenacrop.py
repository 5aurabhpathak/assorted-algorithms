#!/bin/env python3.5
from matplotlib import pyplot as pl
from cv2 import resize, INTER_LANCZOS4
from numpy import cos, sin, matrix, zeros, radians

def resizeto(A, res):
    pl.figure(str(res[0]) + 'x' + str(res[1]))
    pl.imshow(resize(A, res, interpolation=INTER_LANCZOS4))

def crop(A, s, c):
    output = zeros(s, 'uint8')
    for i in range(output.shape[0]):
        for j in range(output.shape[1]): output[i,j] = A[c[0] - output.shape[0]/2 + i, c[1] - output.shape[1]/2 + j, :]
    return output

B = pl.imread('data/lena.png')
resizeto(B, (100, 120))
resizeto(B, (600, 512))
resizeto(B, (1024, 1024))
pl.show()

pl.imshow(crop(B, (300, 300, 3), (B.shape[0]/2, B.shape[1]/2)))
pl.show()

def imrotate(im, angle):
    angle = radians(angle)
    romat, output, adjust = matrix([[cos(angle), sin(angle)],[-sin(angle), cos(angle)]]), zeros(im.shape), matrix([[im.shape[0]/2, im.shape[1]/2]])
    for y in range(im.shape[0]):
        for x in range(im.shape[1]):
            new = (([[y,x]] - adjust) * romat + adjust).astype('int16')
            if all(t >= 0 for t in new.tolist()[0]):
                try: output[new[0,0], new[0,1]] = im[y, x]
                except IndexError: pass
    return output

pl.imshow(imrotate(B, 45))
pl.show()

