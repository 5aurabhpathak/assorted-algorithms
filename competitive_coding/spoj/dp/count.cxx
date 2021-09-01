#include <cstdio>
using namespace std;

int main()
{
	const int MOD = 1988;
	static int n, k, dp[5001][5001];
	for (int i = 0; i <= 5000; i++) dp[0][i] = 1, dp[i][0] = 0;
	for (int i = 1; i <= 5000; i++)
		for (int j = 1; j <= 5000; j++)
			if ((dp[i][j] = dp[i][j-1] + (i-j>=0?dp[i-j][j]:0)) >= MOD) dp[i][j] -= MOD;
	scanf("%d%d", &n, &k);
	while (n) printf("%d\n", dp[n-k][k]), scanf("%d%d", &n, &k);
}
