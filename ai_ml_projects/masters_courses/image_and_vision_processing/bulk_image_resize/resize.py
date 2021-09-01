#!/bin/env python3.5
#Phoenix
from matplotlib import pyplot as pl
from cv2 import resize
from os import listdir, makedirs

target_frame = 400, 400 #adjust to desired frame and run again

def new_size(size): #keeps aspect ratio
    aspect = size[1] / size[0]
    if aspect > 1:
        x = target_frame[1]
        y = int(x / aspect)
    else:
        y = target_frame[0]
        x = int(y * aspect)
    return x, y

makedirs('data/resized', exist_ok=True)
for fname in listdir('data/input'):
    if '.png' not in fname: continue
    im = pl.imread(fname)
    pl.imsave('data/resized/'+fname, resize(im, new_size(im.shape)))
