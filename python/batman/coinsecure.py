#Author: Saurabh Pathak
#Bot
import ccxt, time, ssl
from ccxt.base import errors
from threading import Thread, Event

class Exchange(ccxt.coinsecure):
    def __init__(self):
        self.data, self.updated = None, Event()
        super().__init__()
        
    def check_for_update(self):
        def thread_exec():
            prevTimestamp = None
            while True:
                try:
                    response = self.fetchTicker('BTC/INR')
                    if response['timestamp'] != prevTimestamp:
                        self.data, prevTimestamp = response['info'], response['timestamp']
                        print(self.data)
                        self.updated.set()
                        print('Notifying predictor')
                except (ssl.SSLEOFError, errors.RequestTimeout): print('Non-fatal error occured.')
                time.sleep(2)
        thread = Thread(target=thread_exec)
        thread.start()
