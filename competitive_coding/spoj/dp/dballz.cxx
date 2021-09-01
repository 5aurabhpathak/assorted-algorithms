#include <cstdio>
using namespace std;

int main()
{
	int t, l, k, c[1000], dp[1000001];
	long e, w[1000];
	scanf("%d", &t);
	dp[0] = 0;
	while (t--) {
		scanf("%ld%d", &e, &l);
		for (int i = 0; i < l; i++) scanf("%ld", w+i);
		for (int i = 0; i < l; i++) scanf("%d", c+i);
		for (int i = 1; i <= e; i++) {
			dp[i] = 0;
			for (int j = 0; j < l; j++)
				if (w[j] <= i && (k = c[j] + dp[i-w[j]]) > dp[i]) dp[i] = k;
		}
		printf("%d\n", dp[e]);
	}
}
