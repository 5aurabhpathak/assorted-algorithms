#include <cstdio>
using namespace std;
int main()
{
	int t;
	long n, k;
	scanf("%d", &t);
	float dp[547][1909] = {1.0f}; //normal distribution bounds when p(x) < 0.01, ans = 0
	for (long i = 1l; i <= 546; i++)
		for (long j = i; j <= 1908; j++) {
			for (int l = 1; j >= l && l <= 6; l++)
				dp[i][j] += dp[i-1l][j-l];
			dp[i][j] /= 6.0f;
		}
	while (scanf("%ld%ld", &n, &k) != EOF) {
		if ((n > k) || (k > 6 * n) || ((n > 546) && (k > 1908)))
			printf("%d\n", 0);
		else printf("%d\n", int(dp[n][k] * 100.0f));
	}
}
