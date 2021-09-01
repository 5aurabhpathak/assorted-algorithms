#!/bin/env python3.5
(w, n), wt, v = (map(int, input().split())), [], []
for _ in range(n):
        a,b = map(int, input().split())
        wt += a,
        v += b,

mem = [[0 for _ in range(w+1)] for _ in range(n+1)]
def knapsack(n, w, wt, v):
    if n == 0 or w == 0: return 0
    if mem[n][w] != 0: return mem[n][w]
    if wt[n-1] > w: mem[n][w] = knapsack(n-1, w, wt, v)
    else: mem[n][w] = max(v[n-1] + knapsack(n-1, w - wt[n-1], wt, v), knapsack(n-1, w, wt, v))
    return mem[n][w]

print(knapsack(n, w, wt, v))
