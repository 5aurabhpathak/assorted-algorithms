#Author: Saurabh Pathak
#Bot
import ccxt, abc, time, ssl
from ccxt.base import errors
from statistics import mean
from threading import Thread, Event
from matplotlib import pyplot as pl

class Exchange(ccxt.coinsecure):
    def __init__(self):
        self.data = None
        super().__init__()
        
    def check_for_update(self):
        def thread_exec():
            prevTimestamp = None
            while True:
                try:
                    print('Sending query to exchange...')
                    response = self.fetchTicker('BTC/INR')
                    if response['timestamp'] != prevTimestamp:
                        self.data, prevTimestamp = response['info'], response['timestamp']
                        print(self.data)
                        updated.set()
                        print('Notifying predictor')
                except (ssl.SSLEOFError, errors.RequestTimeout): print('Non-fatal error occured.')
                time.sleep(2)
        thread = Thread(target=thread_exec)
        thread.start()

class Plot(Thread):
    def __init__(self, exchange, predictor):
        self.fig, self.exchange, self.predictor = pl.figure('Live'), exchange, predictor
        self.__handles, self.__lines = [], []
        super().__init__()

    def run(self, *, live_attributes=None, predict_sp=True, predict_bp=True):
        if live_attributes is None: live_attributes = 'bid', 'ask'
        lines = [list() for x in range(len(live_attributes))]
        if predict_sp or predict_bp:
            markermap = {-1: 'v', 0: '_', 1: '^'}
            if predict_bp: bp_points, lbp = [], 0
            if predict_sp: sp_points, lsp = [], 0
        while True:
            updated.wait()
            if predict_sp or predict_bp: predicted.wait()
            print('Plotter received notify.')
            if predict_bp:
                bp_points.append(colourmap[self.predictor.predict_bp])
                lbp += 1
            if predict_sp:
                sp_points.append(colourmap[self.predictor.predict_sp])
                lsp += 1
            for i, x in enumerate(live_attributes):
                lines[i].append(self.exchange.data[x])
                pl.plot(lines[i])
                if x == 'bid' and predict_bp:
                    pointsnumpy.vstack(list(range(lbp)), lines[i])
                    pl.scatter(, c='r', marker='v')
                if x == 'ask' and predict_sp:
                    pl.scatter(list(range(lsp)), lines[i], c=sp_points)
            self.fig.canvas.draw()
            predicted.clear()
            time.sleep(2)

class Classifier(abc.ABC):
    def __init__(self, exchange): self.exchange, self.predict_sp, self.predict_bp = exchange, None, None
    
    @abc.abstractmethod
    def predict(self): pass

class _Window(list):
    def __init__(self, window_size=20):
        self.__window_size, self.__actual_window_size = window_size, 0
        super().__init__()
        
    def append(self, price):
        super().append(price)
        if self.__window_size > self.__actual_window_size: self.__actual_window_size += 1
        else: del self[0]
            
class SMA(Classifier):
    def __init__(self, exchange, *, window_size=20):
        self.__window_size =  window_size
        self.__sp_window, self.__bp_window = _Window(window_size), _Window(window_size)
        super().__init__(exchange)
    
    def predict(self):
        def classify(avg, price):
            if price < avg: return -1
            if price > avg: return 1
            return 0
        
        def thread_exec():
            sp, bp = None, None
            while True:
                updated.wait()
                print('Predictor received notify')
                if sp != self.exchange.data['ask']:
                    sp = self.exchange.data['ask']
                    self.__sp_window.append(sp)
                    self.predict_sp = classify(mean(self.__sp_window), sp)
                if bp != self.exchange.data['bid']:
                    bp = self.exchange.data['bid']
                    self.__bp_window.append(bp)
                    self.predict_bp = classify(mean(self.__bp_window), bp)
                print(self.__sp_window, self.__bp_window)
                print('sp: {}'.format(self.predict_sp), 'bp: {}'.format(self.predict_bp))
                predicted.set()
                updated.clear()
                print('Waiting for notify')
        thread = Thread(target=thread_exec)
        thread.start()

exchange, updated, predicted = Exchange(), Event(), Event()
exchange.checkForUpdate()
predictor = SMA(exchange, window_size=3)
predictor.predict()
plot = Plot(exchange, predictor)
plot.start()
pl.show()
