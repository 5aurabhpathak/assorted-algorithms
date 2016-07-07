#!/bin/env python3
'''http://www.spoj.com/problems/LIS2/'''
n, a, b = int(input()), [], (map(int, input().split()))

def add(t):
    global a
    c = [l for l in a if l[-1] < t]
    if len(c) > 0:
        lens = [len(l) for l in c]
        l = c[lens.index(max(lens))].copy()
        l += t,
        a += l,
    else: a += [t],


for x in b:
    add(x)
    print(a)
print(max([len(x) for x in a]))
