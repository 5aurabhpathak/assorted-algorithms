#!/bin/env python3.5
from matplotlib import pyplot as pl
from numpy import dstack, hstack, vstack, zeros, asarray, sum, matrix, sqrt, square

def edge_filter(kind='prewitt', orientation='h'):
    mask = matrix(zeros((3, 3)))
    mask[0,:], mask[2,:] = -1, 1
    if kind == 'sobel': mask[0, 1], mask[2, 1] = -2, 2
    if orientation == 'v': return asarray(mask.T)
    return asarray(mask)

def convolve(im, mask):

    def pad(im):
        padvert, padhoriz = zeros((im.shape[0], 1)), zeros((1, im.shape[1]+2))
        return vstack((padhoriz, hstack((padvert, im, padvert)), padhoriz))

    im = pad(im)
    out = zeros((im.shape[0], im.shape[1]))
    for i in range(1, im.shape[0] - 1):
        for j in range(1, im.shape[1] - 1):
            out[i,j] = sum(mask * im[i-1:i+2, j-1:j+2])
    return out[1:out.shape[0]-1, 1:out.shape[1]-1]

def process(im):
    r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
    horiz_prewitt_mask, vert_prewitt_mask, horiz_sobel_mask, vert_sobel_mask = edge_filter(), edge_filter(orientation='v'), edge_filter('sobel'), edge_filter('sobel', orientation='v')

    def calclate(s):
    
        def show(im, s):
            pl.figure(s)
            pl.imshow(im.astype('uint8'), 'Greys_r')

        def grad(gx, gy): return sqrt(square(gx) + square(gy))

        hm, vm = (horiz_prewitt_mask, vert_prewitt_mask) if s == 'Prewitt' else (horiz_sobel_mask, vert_sobel_mask)
        edges_hr, edges_hg, edges_hb = convolve(r, hm), convolve(g, hm), convolve(b, hm)
        edges_rv, edges_gv, edges_bv = convolve(r, vm), convolve(g, vm), convolve(b, vm)
        edges_r, edges_g, edges_b = grad(edges_hr, edges_rv), grad(edges_hg, edges_gv), grad(edges_hb, edges_bv)
        show(edges_r, s+' - Red channel')
        show(edges_g, s+' - Green channel')
        show(edges_b, s+' - Blue channel')
        pl.figure(s+' - All channel')
        pl.imshow(dstack((edges_r, edges_g, edges_b)).astype('int8'))
        pl.show()

    calclate('Prewitt')
    calclate('Sobel')

football, peppers = pl.imread('data/football.jpg').astype('int32'), pl.imread('data/peppers.png').astype('int32')
process(peppers)
process(football)
