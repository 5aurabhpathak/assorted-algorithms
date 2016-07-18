#include <cstdio>
using namespace std;

int main()
{
	int t;
	long n;
	long long k, a[100001], dp[100000];
	a[0] = 0ll;
	scanf("%d", &t);
	while (t--) {
		scanf ("%ld", &n);
		for (int i = 1; i <= n; ++i) {
			scanf("%lld", a+i);
			a[i] += a[i-1];
		}
		for (int i = n-1; i >= 0; ++i) {
			dp[i] = 0ll;
			for (int j = 1; j <= 3; j++)
				if (i + j <= n && (k = a[i+j] - a[i] + (i+(j<<1)<n ? dp[i+(j<<1)] : 0ll)) > dp[i]) dp[i] = k;
		}
		printf("%lld\n", dp[0]);
	}
}
