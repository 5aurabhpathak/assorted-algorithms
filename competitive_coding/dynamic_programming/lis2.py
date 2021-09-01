#!/bin/env python3
class MyTuple(tuple):

    def __gt__(self, other):
        if self[0] > other[0] and self[1] > other[1]: return True
        return False

n, a, mem = int(input()), [], [1]
for i in range(n): a += MyTuple(map(int, input().split())),
for i in range(1, n):
    mem += 1,
    for j in range(i):
        if a[i] > a[j] and mem[j] >= mem[i]: mem[i] += 1
print(max(mem))
