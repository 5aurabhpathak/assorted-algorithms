#include <climits>
#include <cmath>
#include <cstdio>
#include <cstring>
using namespace std;

int a[16], b[16], dp[1<<16], n;

int solve(int);
int main()
{
	scanf("%d", &n);
	while (n) {
		for (int i = 0; i < n; i++) scanf("%d", a+i);
		for (int i = 0; i < n; i++) scanf("%d", b+i);
		memset(dp, -1, (1<<n) * sizeof(int));
		printf("%d\n", solve(0));
		scanf("%d", &n);
	}
}

int solve(int m)
{
	if (dp[m] != -1) return dp[m];
	if (m == (1<<n)-1) return dp[m] = 0;
	dp[m] = INT_MAX;
	int r = n, t = m;
	while (t) {
		r -= t & 1;
		t >>= 1;
	}
	for (int i = 0; i < n; i++)
		if (!(m & (1<<i))) {
			int p = abs(r-1-i) + abs(a[r-1]-b[i]) + solve(m | (1<<i));
			if (p < dp[m]) dp[m] = p;
		}
	return dp[m];
}
