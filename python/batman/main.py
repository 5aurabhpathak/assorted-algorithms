from configparser import RawConfigParser, NoSectionError
from coinsecure import Exchange
from sma import SMA
from visualize import Plot
from matplotlib import pyplot as pl

class _Predictor_Factory(RawConfigParser):
	def __init__(self):
		super().__init__(allow_no_value=True)
		self.read('settings.conf')

	def create(self, exchange):
		pred = self.items('Predictor')[0][0].upper()
		try: opts = dict(self.items(pred))
		except NoSectionError: raise NotImplementedError('{} is not implemented yet!'.format(pred))
		if pred == 'SMA':
			from sma import SMA
			return SMA(exchange, **opts) 
		#to do -- other predictors

if __name__  == '__main__':
	exchange = Exchange()
	exchange.checkForUpdate()
	predictor = _Predictor_Factory().create(exchange)
	predictor.predict()
	plot = Plot(exchange, predictor)
	plot.start()
	pl.show()
