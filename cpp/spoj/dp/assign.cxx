#include <cstdio>
#include <cstring>
using namespace std;

bool a[20][20];
int n;

void solve();
int main()
{
	int c;
	scanf("%d", &c);
	while (c--) {
		scanf("%d", &n);
		for (int i = 0; i < n; i++)
			for (int j = 0; j < n; j++) scanf("%d", a[i]+j);
		solve();
	}
}

void solve()
{
	long long dp[1<<20];
	memset(dp, 0, (1<<n) * sizeof(long long));
	long C = (1<<n)-1;
	dp[C] = 1ll;
	for (long m = C-1; m >= 0; m--) {
		long t = m;
		int r = n;
		while (t) {
			r -= t & 1;
			t >>= 1;
		}
		for (int i = 0; i < n; i++)
			if (a[r-1][i] && !(m & 1<<i)) dp[m] += dp[m | 1<<i];
	}
	printf("%lld\n", dp[0]);
}
