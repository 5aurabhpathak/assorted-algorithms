#!/bin/env python3.5
#Author: Saurabh Pathak
from matplotlib import pyplot as pl
from mpl_toolkits.mplot3d import Axes3D
from numpy import meshgrid, zeros

class Fuzzer:

    def __init__(self, inc, const, dec):
        if inc is not None:
            self.mi = 1 / (inc[1] - inc[0])
            self.ci = - self.mi * inc[0]
        if dec is not None:
            self.md = -1 / (dec[1] - dec[0])
            self.cd = - self.md * dec[1]
        self.const, self.inc, self.dec = const, inc, dec
        self.beg = inc[0] if inc is not None else const[0] if const is not None else dec[0]
        self.end = dec[1] if dec is not None else const[1] if const is not None else inc[1]

    def fuzzify(self, value):
        if self.const is not None and self.const[0] <= value <= self.const[1]: return 1
        elif self.inc is not None and self.inc[0] <= value <= self.inc[1]: return self.mi * value + self.ci
        elif self.dec is not None and self.dec[0] <= value <= self.dec[1]: return self.md *value + self.cd
        return 0

class DeFuzzer:

    def __init__(self, step, Fuzzers):
        self.Fuzzers = Fuzzers
        self.step = step

    #defuzzification using CoG - Mamdani method
    def defuzzify(self, tup):
        numerator, denominator = 0, 0
        for f, v in zip(self.Fuzzers, tup):
            d = 0
            for s in range(f.beg, f.end + 1, self.step):
                d += s
                denominator += v
            numerator += d * v
        return numerator / denominator

class FuzzyEvaluator:

    def __init__(self, InputFuzzerSets, OutputFuzzerSets, rules, outputstepSet):
        self.InputFuzzerSets = InputFuzzerSets
        self.OutputFuzzerSets = OutputFuzzerSets
        self.rules = rules
        self.outputstepSet = outputstepSet

    def evaluate(self, *inputs):
        ipfuz, op = [], []
        for ip, ifuzzers in zip(inputs, self.InputFuzzerSets): ipfuz += [f.fuzzify(ip) for f in ifuzzers],
        for out, ofs, step in zip(self.rules(*ipfuz), self.OutputFuzzerSets, self.outputstepSet): op += DeFuzzer(step, ofs).defuzzify(out),
        return op

#home evaluation
MVFuzzers = Fuzzer(None, (0,5), (5,10)), Fuzzer((5,10), (10,20), (20,30)), Fuzzer((20,30), (30,65), (65,85)), Fuzzer((65,85), (85,100), None)
LocFuzzers = Fuzzer(None, (0,1.5), (1.5,4)), Fuzzer((2.5,5), (5,6), (6,8.5)), Fuzzer((6,8.5), (8.5,10), None)
HouseFuzzers = Fuzzer(None, None, (0,3)), Fuzzer((0,3), None, (3,6)), Fuzzer((2,5), None, (5,8)), Fuzzer((4,7), None, (7,10)), Fuzzer((7,10), None, None)

def rulebase_home(mval, loc):
    house = [0, 0, 0, 0, 0]
    if mval[0] != 0: house[1] = mval[0]
    if loc[0] != 0: house[1] = loc[0]
    if loc[0] != 0 and mval[0] != 0: house[0] = min(loc[0], mval[0])
    if loc[0] != 0 and mval[1] != 0: house[1] = min(loc[0], mval[1])
    if loc[0] != 0 and mval[2] != 0: house[2] = min(loc[0], mval[2])
    if loc[0] != 0 and mval[3] != 0: house[3] = min(loc[0], mval[3])
    if loc[1] != 0 and mval[0] != 0: house[1] = min(loc[1], mval[0])
    if loc[1] != 0 and mval[1] != 0: house[2] = min(loc[1], mval[1])
    if loc[1] != 0 and mval[2] != 0: house[3] = min(loc[1], mval[2])
    if loc[1] != 0 and mval[3] != 0: house[4] = min(loc[1], mval[3])
    if loc[2] != 0 and mval[0] != 0: house[2] = min(loc[2], mval[0])
    if loc[2] != 0 and mval[1] != 0: house[3] = min(loc[2], mval[1])
    if loc[2] != 0 and mval[2] != 0: house[4] = min(loc[2], mval[2])
    if loc[2] != 0 and mval[3] != 0: house[4] = min(loc[2], mval[3])
    return house,

mval, loc = map(int, input('Enter market value(max 100) and location(max 10):').split())
house  = FuzzyEvaluator((MVFuzzers, LocFuzzers), (HouseFuzzers,), rulebase_home, (1,)).evaluate(mval, loc)[0]
print('House:', house)

#Applicant evaluation
AssetFuzzers = Fuzzer(None, None, (0,150)), Fuzzer((50,250), (250,450), (450,650)), Fuzzer((500,700), (700,1000), None)
IncFuzzers = Fuzzer(None, (0,10), (10,25)), Fuzzer((15,35), None, (35,55)), Fuzzer((40,60), None, (60,80)), Fuzzer((60,80), (80,100), None)
AppFuzzers = Fuzzer(None, (0,2), (2,4)), Fuzzer((2,5), None, (5,8)), Fuzzer((6,8), (8,10), None)

def rulebase_app(asset, inc):
    app = [0, 0, 0]
    if asset[0] != 0 and inc[0] != 0: app[0] = min(asset[0], inc[0])
    if asset[0] != 0 and inc[1] != 0: app[0] = min(asset[0], inc[1])
    if asset[0] != 0 and inc[2] != 0: app[1] = min(asset[0], inc[2])
    if asset[0] != 0 and inc[3] != 0: app[2] = min(asset[0], inc[3])
    if asset[1] != 0 and inc[0] != 0: app[0] = min(asset[1], inc[0])
    if asset[1] != 0 and inc[1] != 0: app[1] = min(asset[1], inc[1])
    if asset[1] != 0 and inc[2] != 0: app[2] = min(asset[1], inc[2])
    if asset[1] != 0 and inc[3] != 0: app[2] = min(asset[1], inc[3])
    if asset[2] != 0 and inc[0] != 0: app[1] = min(asset[2], inc[0])
    if asset[2] != 0 and inc[1] != 0: app[1] = min(asset[2], inc[1])
    if asset[2] != 0 and inc[2] != 0: app[2] = min(asset[2], inc[2])
    if asset[2] != 0 and inc[3] != 0: app[2] = min(asset[2], inc[3])
    return app,

asset, inc = map(int, input('Enter assets(max 1000) and income(max 100):').split())
app = FuzzyEvaluator((AssetFuzzers, IncFuzzers), (AppFuzzers,), rulebase_app, (1,)).evaluate(asset, inc)[0]
print('Applicant:', app)

#Credit evaluation
InterestFuzzers = Fuzzer(None, (0,2), (2,5)), Fuzzer((2,4), (4,6), (6,8)), Fuzzer((6,8.5), (8.5,10), None)
CreditFuzzers = HouseFuzzers

def rulebase_cred(inc, intr, app, house):
    cred = [0, 0, 0, 0, 0]
    if inc[0] != 0 and intr[1] != 0: cred[0] = min(inc[0], intr[1])
    if inc[0] != 0 and intr[2] != 0: cred[0] = min(inc[0], intr[2])
    if inc[1] != 0 and intr[2] != 0: cred[1] = min(inc[1], intr[2])
    if app[0] != 0: cred[0] = app[0]
    if house[0] != 0: cred[0] = house[0]
    if app[1] != 0 and house[0] != 0: cred[1] = min(app[1], house[0])
    if app[1] != 0 and house[1] != 0: cred[1] = min(app[1], house[1])
    if app[1] != 0 and house[2] != 0: cred[2] = min(app[1], house[2])
    if app[1] != 0 and house[3] != 0: cred[3] = min(app[1], house[3])
    if app[1] != 0 and house[4] != 0: cred[3] = min(app[1], house[4])
    if app[2] != 0 and house[0] != 0: cred[1] = min(app[2], house[0])
    if app[2] != 0 and house[1] != 0: cred[2] = min(app[2], house[1])
    if app[2] != 0 and house[2] != 0: cred[3] = min(app[2], house[2])
    if app[2] != 0 and house[3] != 0: cred[3] = min(app[2], house[3])
    if app[2] != 0 and house[4] != 0: cred[4] = min(app[2], house[4])
    return cred,

intr = float(input('Enter interest rate(max 10):'))
print('Credit:', FuzzyEvaluator((IncFuzzers, InterestFuzzers, AppFuzzers, HouseFuzzers), (CreditFuzzers,), rulebase_cred, (1,)).evaluate(inc, intr, app, house)[0])

input('Press Enter...')
mval, loc = meshgrid(range(101), range(11))
FE, house = FuzzyEvaluator((MVFuzzers, LocFuzzers), (HouseFuzzers,), rulebase_home, (1,)), zeros(1111)
for m, l, i in zip(mval.ravel(), loc.ravel(), range(1111)): house[i] = FE.evaluate(m, l)[0]

fig1 = pl.figure('Plot for rulebase-1')
ax = pl.subplot(projection='3d')
ax.set_xlabel('Market Value (x10^4 $)')
ax.set_ylabel('Location')
ax.set_zlabel('House')
fig1.colorbar(ax.plot_surface(mval, loc, house.reshape(mval.shape), cmap='coolwarm', rstride=1, cstride=1, linewidth=0))

asset, inc = meshgrid(range(0, 1001, 30), range(101))
FE, app = FuzzyEvaluator((AssetFuzzers, IncFuzzers), (AppFuzzers,), rulebase_app, (1,)), zeros(3434)
for a, incm, i in zip(asset.ravel(), inc.ravel(), range(101101)): app[i] = FE.evaluate(a, incm)[0]

fig2 = pl.figure('Plot for rulebase-2')
ax = pl.subplot(projection='3d')
ax.set_xlabel('Assets (x10^3 $)')
ax.set_ylabel('Income (x10^3 $)')
ax.set_zlabel('Applicant')
fig2.colorbar(ax.plot_surface(asset, inc, app.reshape(asset.shape), cmap='coolwarm', rstride=1, cstride=1, linewidth=0))

pl.show()
