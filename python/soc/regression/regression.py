#!/bin/env python3
from matplotlib import pyplot as pl
import pandas as pd
df = pd.read_csv('/home/phoenix/csv/sortediris.csv', header=None)
df.plot(x=0, y=1, kind='scatter')
res = pd.ols(y=df[1], x=df[0])
pl.plot(res.x['x'], res.y_fitted)
pl.show()
