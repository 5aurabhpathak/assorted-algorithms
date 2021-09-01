#!/bin/env python3
from matplotlib import pyplot as pl
import csv, sys

def readIntoList(fname):
    if fname in {'', None}:
        fname = '/home/phoenix/csv/BP.csv'
    try:
        return list(csv.reader(open(fname)))
    except FileNotFoundError as e:
        print(e)
        return readIntoList(input('Enter absolute file name or enter to load BP.csv:'))

def getColumn(r, index):
    try:
        return [float(row[index]) for row in r]
    except IndexError as e:
        print(e)
        return getColumn(r, int(input('Enter again:')))

if len(sys.argv) != 4:
    print('Usage: regress_manual.py csvfile xcolumnindex ycolumnindex')
    quit(1)

dataset = readIntoList(sys.argv[1])

success = False
while not success:
    try:
        x = getColumn(dataset, int(sys.argv[2]))
        y = getColumn(dataset, int(sys.argv[3]))
        success = True
    except ValueError as e:
        print(e, '\nUsage: regression_manual.py csvfile xcolumnindex ycolumnindex')
        quit(1)


def createFigure(figNum, title):
	pl.figure(figNum)
	pl.xlabel('x')
	pl.ylabel('y')
	pl.title(title)
	pl.scatter(x, y)

def drawFigure(fignum, *args):
	pl.figure(fignum)
	pl.plot(*args)

#manual SSE calculation begin

xbar = sum(x) / len(x)
ybar = sum(y) / len(y)
sumxy = sum([a*b for (a, b) in zip(x, y)])
sumxsquare = sum([a*a for a in x])

b = (sumxy - len(x) * xbar * ybar) / (sumxsquare - len(x) * xbar ** 2)
a = ybar - b * xbar

ypredicted = [a + b * xval for xval in x]

pl.ion()
createFigure('Y on X', 'Regression of y on x')
createFigure('X on Y', 'Regression of x on y')
createFigure('Overlay', 'Regression')

drawFigure('Y on X', x, ypredicted)
pl.savefig('data/yonx.png', format='png')
drawFigure('Overlay', x, ypredicted)

#xony

xony=pl.figure(2)
pl.scatter(x, y)

sumysquare = sum([a*a for a in y])
b *= (sumxsquare - len(x) * xbar ** 2) / (sumysquare - len(y) * ybar ** 2)
a = xbar - b * ybar

xpredicted = [a + b * yval for yval in y]

drawFigure('X on Y', xpredicted, y)
pl.savefig('data/xony.png', format='png')
drawFigure('Overlay', xpredicted, y)
pl.savefig('data/overlayed.png', format='png')
pl.ioff()
pl.show()
pl.close()
pl.close('X on Y')
pl.close('Y on X')
