from threading import Event
from abc import ABC, abstractmethod

class Classifier(ABC):
    def __init__(self, exchange): self.predicted, self.exchange, self.predict_sp, self.predict_bp = Event(), exchange, None, None
    
    @abstractmethod
    def predict(self): pass
