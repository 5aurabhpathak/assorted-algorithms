from matplotlib import pyplot as pl
from numpy import zeros, sqrt, around

def display(im, cmap='Greys_r'):
    pl.imshow(im, cmap=pl.get_cmap(cmap))
    pl.axis('off')
    pl.show()

im = []
for i in range(256): im += [i]*256,
display(im)

def draw_circle(im, centre, radius):
    '''Bresenham's circle drawing algorithm'''
    for i in range(int(around(radius / sqrt(2), decimals=0) + 1)):
        k = int(around(sqrt(radius**2 - i**2), decimals=0))
        im[centre[0] + i, centre[1] + k] = im[centre[0] - i, centre[1] - k] = im[centre[0] + k, centre[1] +i] = im[centre[0] - k, centre[1] - i] = im[centre[0] +i, centre[1] - k] = im[centre[0] - i, centre[1] + k] = im[centre[1] - k , centre[0] + i] = im[centre[1] + k, centre[0] - i] = True


im = zeros((256, 256), bool)
draw_circle(im, (128, 128), 50)
display(im, 'binary_r')

cam = pl.imread('data/cameraman.tif')
croppedcam = zeros((256,256))
for i in range(cam.shape[0]):
    for j in range(cam.shape[1]):
        if im[i,j] or (any(im[i, :j]) and any(im[i, j:])): croppedcam[i,j] = cam[i,j]

display(croppedcam)

draw_circle(im, (128, 128), 100)
for i in range(im.shape[0]):
    boundary = False
    x = []
    for j in range(im.shape[1]):
        if not boundary and im[i,j]:
            boundary =  True
            x += j,
        elif boundary and not im[i,j]:
            boundary = False
    if len(x) > 1:
        im[i, x[0]:x[1]] = True
    if len(x) == 3:
        im[i, x[1]:x[2]] = True
    elif len(x) > 3:
        im[i, x[2]:x[3]] = True

display(im, 'binary_r')
