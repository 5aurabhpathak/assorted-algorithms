# coding: utf-8

import ccxt, abc, time, ssl
from statistics import mean
from threading import Thread, Event
from matplotlib import pyplot as pl

updated = Event()

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
                    if response['timestamp']:
                        self.data, prevTimestamp = response['info'], response['timestamp']
                        print(self.data)
                        updated.set()
                        print('Notifying predictor')
                except ssl.SSLEOFError: print('Non-fatal error occured.')
                time.sleep(2)
        thread = Thread(target=thread_exec)
        thread.start()

class Plot(Thread):
    def __init__(self):
        self.fig = pl.figure('Live')
        self.__handles, self.__lines = [], []
        super().__init__()
    
    def attach(self, data): self.__handles.append(data), self.__lines.append([])
    
    def run(self):
        while True:
            updated.wait()
            for i, x in enumerate(self.__handles): self.__lines[i].append(eval(x))
            for x in self.__lines: pl.plot(x)
            self.fig.canvas.draw()
            time.sleep(2)

class Classifier(abc.ABC):
    def __init__(self, exchange): self.exchange = exchange
    
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
        self.__window_size, self.predict_sp, self.predict_bp = window_size, None, None
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
                    predict_sp = classify(mean(self.__sp_window), sp)
                if bp != self.exchange.data['bid']:
                    bp = self.exchange.data['bid']
                    self.__bp_window.append(bp)
                    predcit_bp = classify(mean(self.__bp_window), bp)
                print(self.__sp_window, self.__bp_window)
                print('sp: {}'.format(predict_sp), 'bp: {}'.format(predcit_bp))
                updated.clear()
                print('Waiting for notify')
        thread = Thread(target=thread_exec)
        thread.start()

exchange = Exchange()
exchange.checkForUpdate()
predictor = SMA(exchange, window_size=3)
predictor.predict()
plot = Plot()
updated.wait()
plot.attach("exchange.data['bid']")
plot.attach('predictor.predict_bp')
plot.start()
pl.show()

