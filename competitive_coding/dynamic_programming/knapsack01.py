#!/bin/env python3.5
(w, n), wt, v = (map(int, input().split())), [], []
for _ in range(n):
        a,b = map(int, input().split())
        wt += a,
        v += b,

def knapsack(n, w, wt, v):
        dp = [[0]*(w+1)]
        dp += [[(0 if j == 0 else (dp[i][j-1] if wt[j-1] > j else max(dp[i][j-1], v[j-1] + dp[i-1][j-wt[j-1]]))) for j in range(w+1)]for i in range(1, n+1)]
        return dp[n][w]

print(knapsack(n, w, wt, v))
