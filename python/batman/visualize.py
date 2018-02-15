import numpy
from matplotlib import pyplot as pl
from threading import Thread

class Plot(Thread):
    def __init__(self, exchange, predictor, *, live_attributes=('bid', 'ask'), predict_sp=True, predict_bp=True):
        self.__figures, self.exchange, self.predictor, self.__lines = None, exchange, predictor, []
        self.__predict_sp, self.__predict_bp, self.__live_attributes = predict_sp, predict_bp, live_attributes
        for x in live_attributes:
            pl.figure('Live {}'.format(x))
            pl.xlim(xmin=0)
            pl.ticklabel_format(axis='y', style='plain')
        super().__init__()
        
    def run(self):
        def helper(arr, arr_col, val):
            x, = numpy.nonzero(arr == val)
            pl.scatter(x, lines[i][x], c=arr_col, marker=markermap[val])

        def choose_colour(arr, arr_col):
            try:
                if ((lines[i][-2] > lines[i][-1] and arr[-1] == -1) or
                    (lines[i][-2] < lines[i][-1] and arr[-1] == 1) or
                    (lines[i][-2] == lines[i][-1] and arr[-1] == 0)): arr_col[-1] = 'g'
                else: arr_col[-1] = 'r'
            except IndexError: pass
            arr_col = numpy.append(arr_col, 'y')
            return arr_col

        markermap = {-1: 'v', 0: 'o', 1:'^'}
        lines = [numpy.empty(0) for x in self.__live_attributes]
        if self.__predict_bp: bp_y, bp_colours = numpy.empty(0), numpy.empty(0)
        if self.__predict_sp: sp_y, sp_colours = numpy.empty(0), numpy.empty(0)
        while True:
            self.exchange.updated.wait()
            if self.__predict_sp or self.__predict_bp:
                self.predictor.predicted.wait()
                if self.__predict_bp: bp_y = numpy.append(bp_y, self.predictor.predict_bp)
                if self.__predict_sp: sp_y = numpy.append(sp_y, self.predictor.predict_sp)
            print('Plotter received notify.')
            for i, a in enumerate(self.__live_attributes):
                pl.figure('Live {}'.format(a))
                lines[i] = numpy.append(lines[i], self.exchange.data[a]/100)
                pl.plot(lines[i])
                if a == 'bid' and self.__predict_bp:
                    bp_colours = choose_colour(bp_y, bp_colours)
                    helper(bp_y, bp_colours, -1), helper(bp_y, bp_colours, 0), helper(bp_y, bp_colours, 1)
                if a == 'ask' and self.__predict_sp:
                    sp_colours = choose_colour(sp_y, sp_colours)
                    helper(sp_y, sp_colours, -1), helper(sp_y, sp_colours, 0), helper(sp_y, sp_colours, 1)
                pl.gcf().canvas.draw()
            if self.__predict_sp or self.__predict_bp: self.predictor.predicted.clear()
