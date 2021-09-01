#include <cstdio>
using namespace std;

bool ar[1000][1000];

long solve(int, int);
int main()
{
	int k, m, n;
	long max, t;
	char c;
	scanf("%d", &k);
	while (k--) {
		max = 0l;
		scanf("%d%d", &m, &n);
		for (int i = 0; i < m; i++)
			for (int j = 0; j < n; j++) {
				scanf(" %c", &c);
				if ((ar[i][j] = c=='F') && (t = solve(i, j)) > max) max = t;
			}
		printf("%ld\n", 3l * max);
	}
}

long solve(int a, int b)
{
	long max = 0l, dp[1000][1000];
	for (int i = a; i >= 0; i--)
		for (int j = b; j >= 0; j--) {
			if (i < a && j < b) dp[i][j] = dp[i][j+1]&&dp[i+1][j]&&ar[i][j] ? dp[i][j+1]+dp[i+1][j]-dp[i+1][j+1]+ar[i][j] : 0l;
			else if (i < a && j == b) dp[i][j] = dp[i+1][j]&&ar[i][j] ? dp[i+1][j]+ar[i][j] : 0l;
			else if (i == a && j < b) dp[i][j] = dp[i][j+1]&&ar[i][j] ? dp[i][j+1]+ar[i][j] : 0l;
			else dp[i][j] = ar[i][j];
			if (!dp[i][j]) break;
			if (dp[i][j] > max) max = dp[i][j];
		}
	return max;
}
