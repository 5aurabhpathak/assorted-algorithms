#include <cstdio>
using namespace std;


int main()
{
	int t, m, n, a[1000], dp[1000], x, max;
	scanf("%d", &t);
	while (t--) {
		max = 0;
		scanf("%d%d", &n, &m);
		for (int i = 0; i < n; i++) {
			scanf("%d", a+i);
			dp[i] = 1;
			for (int j = 0; j < i; j++)
				if (a[j] > a[i] && (x = dp[j]+1) > dp[i]) dp[i] = x;
			if (i > m && a[i] >= a[m] && (x = dp[m]+1) > dp[i]) dp[i] = x;
			if (dp[i] > max) max = dp[i];
		}
		printf("%d\n", max);
	}
}
