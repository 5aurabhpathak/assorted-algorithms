#include <cstdio>
using namespace std;

int main()
{
	static int t, x, max, i, j, a[2000], b[2000], dp[2001][2001];
	scanf("%d", &t);
	while (t--) {
		i = 0;
		scanf("%d", &x);
		while (x) {
			a[i++] = x;
			scanf("%d", &x);
		}
		max = 0;
		scanf("%d", &x);
		while (x) {
			j = 0;
			b[j++] = x;
			scanf("%d", &x);
			while (x) {
				b[j++] = x;
				scanf("%d", &x);
			}
			for (int k = 1; k <= i; k++)
				for (int l = 1; l <= j; l++) dp[k][l] = a[k-1]==b[l-1] ? 1 + dp[k-1][l-1] : dp[k-1][l]>dp[k][l-1] ? dp[k-1][l] : dp[k][l-1];
			if (dp[i][j] > max) max = dp[i][j];
			scanf("%d", &x);
		}
		printf("%d\n", max);
	}
}
