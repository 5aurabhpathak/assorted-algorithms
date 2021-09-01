#!/bin/env python3
'''http://www.spoj.com/problems/LIS2/'''
import copy
class MyTuple(tuple):

    def __lt__(self, other):
        if self[0] < other[0] and self[1] < other[1]: return True
        return False

n, a = int(input()), []

def add(t):
    global a
    c = [l for l in a if l[0][-1] < t]
    if len(c) > 0:
        l = copy.deepcopy(c[c.index(max(c, key=lambda x: x[1]))])
        l[0] += t,
        l[1] += 1
        a += l,
    else: a += [[t], 1],


for i in range(n): add(MyTuple(map(int, input().split())))
print(max(a, key=lambda x: x[1])[1])
