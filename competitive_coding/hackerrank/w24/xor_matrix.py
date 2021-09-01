n, m = map(int, input().strip().split())
a = list(map(int, input().strip().split()))

def pattern(a, i):
    if i == m-1: return a
    x = 1
    while i + (x << 1) <= m-1: x <<= 1
    return pattern([a[j]^a[(j+x)%n] for j in range(n)], i + x)

for x in pattern(a, 0): print(x, end=' ')
print()
