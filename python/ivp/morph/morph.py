from matplotlib import pyplot as pl
from numpy import matrix, vstack, hstack, zeros, any, logical_and, array_equal, ogrid
from numpy.ma import masked_equal

def move_mask(im, mask, op):
    x = mask.shape[0] // 2

    def pad(im):
        padvert, padhoriz = zeros((im.shape[0], x)), zeros((x, im.shape[1]+2*x))
        return vstack((padhoriz, hstack((padvert, im, padvert)), padhoriz))

    im = pad(im)
    out = zeros((im.shape[0], im.shape[1]))
    for i in range(x, im.shape[0] - x):
        for j in range(x, im.shape[1] - x):
            out[i,j] = op(mask, im[i-x:i+x+1, j-x:j+x+1])
    return out[x:out.shape[0]-x, x:out.shape[1]-x]

def work(im, mask, s):
    pl.figure('SE size: '+s)
    im = pl.imread(im)
    outdilate, outerode = move_mask(im, mask, dilation), move_mask(im, mask, erosion)
    outopen, outclose = move_mask(outerode, mask, dilation), move_mask(outdilate, mask, erosion)

    def show(im, n, t):
        pl.subplot(230+n)
        pl.imshow(im, 'binary_r')
        pl.title(t)
        pl.axis('off')

    show(im, 1, 'Input')
    show(outerode, 2, 'Eroded')
    show(outdilate, 3, 'Dilated')
    show(outopen, 4, 'Opened')
    show(outclose, 5, 'Closed')
    pl.show()

def se(size):
    s = size // 2
    x, y = ogrid[-s:s+1, -s:s+1]
    return x * x + y * y <= s * s

im = 'data/blobs.png'
erosion, dilation = lambda x,y: array_equal(x, logical_and(x,y)), lambda x,y: any(logical_and(x,y))
work(im, se(3), '3X3')
work(im, se(5), '5X5')
work(im, se(7), '7X7')
