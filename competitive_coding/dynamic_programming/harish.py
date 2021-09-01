#!/bin/env python3.5
#http://www.spoj.com/problems/ABA12C/
t = int(input())
dp = [[1000 * 100]*k]*n

def solve(n, k, d):
    if n == 0 or k == 0: return 0

    if d[n] == -1: return solve(n, k - 1, d)

    return min(solve(n, k - 1, d), d[k] + solve(n - 1, k, d))

for _ in range(t):
    n, k = int(input()), int(input())
    d = 
    print(solve(n, k, d))
