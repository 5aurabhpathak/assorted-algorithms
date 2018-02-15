from classifier import Classifier
from threading import Thread
from statistics import mean

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
        window_size = int(window_size) #needed for conf compatibility
        self.__window_size, self.__sp_window, self.__bp_window =  window_size, _Window(window_size), _Window(window_size)
        super().__init__(exchange)
    
    def predict(self):
        def classify(avg, price): return -1 if price < avg else 1 if price > avg else 0
        
        def thread_exec():
            sp, bp = None, None
            while True:
                self.exchange.updated.wait()
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
                self.predicted.set()
                self.exchange.updated.clear()
                print('Waiting for notify')
        thread = Thread(target=thread_exec)
        thread.start()
