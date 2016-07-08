#include <algorithm>
#include <cstdio>
#include <cstring>
using namespace std;

int a[30], dp[2][30][30][2];

int solve(bool, int, int, bool);
int main()
{
	int t, n;
	scanf("%d", &t);
	while (t--) {
		memset(dp, -1, sizeof dp);
		scanf("%d", &n);
		for (int i = 0; i < n; i++) scanf("%d", a+i);
		printf("%d %d\n", solve(true, 0, n-1, true), solve(true, 0, n-1, false));
	}
}

int solve(bool p, int b, int e, bool dumb)
{
	if (b > e) return 0;
	if (dp[p][b][e][dumb] != -1) return dp[p][b][e][dumb];
	if (p) return dp[p][b][e][dumb] = max(a[b]+solve(false, b+1, e, dumb), a[e]+solve(false, b, e-1, dumb));
	return dp[p][b][e][dumb] = dumb? max(solve(true, b+1, e, dumb), solve(true, b, e-1, dumb)) : min(solve(true, b+1, e, dumb), solve(true, b, e-1, dumb));
}
