#include <cstdio>
#include <cstring>
using namespace std;

int main()
{
	long dp[1005][1025], sum;
	const long MOD = 100000007l;
	int t, n, m, a[1025], b[1025],B;
	scanf("%d", &t);
	for (int c = 1; c <= t; c++) {
		memset(dp, 0, sizeof dp);
		memset(b, 0, sizeof b);
		sum = 0l;
		dp[0][0] = 1l;
		scanf("%d%d", &n, &m);
		for (int i = 0; i < n; i++) scanf("%d", a+i);
		for (int i = 1; i <= n; i++)
			for (int j = 0; j < 1024; j++)
				dp[i][j] = (dp[i][j] + dp[i-1][j] + dp[i-1][j^a[i-1]]) % MOD;
		for (int i = 0; i < m; i++) {
			scanf("%d", &B);
			b[B] = 1;
		}
		for (int j = 0; j < 1024; j++)
			if (!b[j]) sum = (sum + dp[n][j]) % MOD;
		printf("Case %d: %ld\n", c, sum);
	}
}
