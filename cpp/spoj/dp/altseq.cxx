#include <cstdio>
using namespace std;

int main()
{
	int n, k, m = 0;
	scanf("%d", &n);
	long *a = new long[n];
	int *dp = new int[n];
	for (int i = 0; i < n; i++) {
		scanf("%ld", a+i);
		dp[i] = 1;
		for (int j = 0; j < i; j++)
			if (((a[i] < 0 && a[j] > 0 && -a[i] > a[j]) || (a[i] > 0 && a[j] < 0 && a[i] > -a[j])) && (k = 1 + dp[j]) > dp[i]) dp[i] = k;
		if (dp[i] > m) m = dp[i];
	}
	printf("%d\n", m);
}
