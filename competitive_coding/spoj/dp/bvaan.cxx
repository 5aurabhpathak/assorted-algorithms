#include <cstdio>
#include <cstring>
using namespace std;

int dp[101][101][101], n1, n2;
char s1[101], s2[101];

int solve(int, int, int);
int main()
{
	int t, k;
	scanf("%d", &t);
	while (t--) {
		scanf("%s%s%d", s1, s2, &k);
		n1 = strlen(s1);
		n2 = strlen(s2);
		for (int i = 0; i <= k; i++)
			for (int j = 0; j <= n1; j++) memset(dp[i][j], -1, (n2+1)*sizeof(int));
		printf("%d\n", solve(k, 0, 0));
	}
}

int solve(int k, int b1, int b2)
{
	if (dp[k][b1][b2] != -1) return dp[k][b1][b2];
	if (!k) return dp[k][b1][b2] = 0;
	int m, &max = dp[k][b1][b2] = 0;
	for (int i = b1; i < n1; i++)
		for (int j = b2; j < n2; j++)
			if (s1[i] == s2[j]) {
				m = solve(k-1, i+1, j+1);
				if ((!m) && (k > 1)) continue;
				if ((m += s1[i]) > max) max = m;
			}
	return max;
}
