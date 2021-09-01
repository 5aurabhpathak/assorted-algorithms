#!/bin/env python3.5
N, A, mem = int(input()), list(map(int, input().split())), [1]
for i in range(1, N):
    mem += 1,
    for j in range(i):
        if A[i] > A[j] and mem[j] >= mem[i]: mem[i] += 1
print(max(mem))
