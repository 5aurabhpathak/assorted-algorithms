#include <cstdio>
#include <cstring>
using namespace std;

int n, m, N[20], c[20][20], w[20][20], dp2[20][1001], dp1[20][1001];

int solve(int, int);
int power(int, int);
int main()
{
	int t, k;
	scanf("%d", &t);
	while (t--) {
		scanf("%d%d%d", &n, &m, &k);
		for (int i = 0; i < n; i++) scanf("%d", N+i);
		for (int i = 0; i < n; i++)
			for (int j = 0; j < m; j++) scanf("%d", *(c+i)+j);
		memset(dp1, -1, sizeof dp1);
		memset(dp2, -1, sizeof dp2);
		for (int i = 0; i < n; i++)
			for (int j = 0; j < m; j++) scanf("%d", *(w+i)+j);
		printf("%d\n", solve(0, k));
	}
}

int solve(int n, int k)
{
	if (dp1[n][k] != -1) return dp1[n][k];
	if (n == ::n || !k) return dp1[n][k] = 0;
	dp1[n][k] = solve(n+1, k);
	int m;
	for (int i = 0; i <= k-N[n]; i++) {
		m = power(n, i) + solve(n+1, k-N[n]-i);
		if (dp1[n][k] < m) dp1[n][k] = m;
	}
	return dp1[n][k];
}

int power(int n, int k)
{
	if (dp2[n][k] != -1) return dp2[n][k];
	dp2[n][k] = 0;
	if (!k) return dp2[n][k];
	int t;
	for (int i = 0; i < m; i++)
		if (k >= c[n][i] && (t = w[n][i] + power(n, k-c[n][i])) > dp2[n][k]) dp2[n][k] = t;
	return dp2[n][k];
}
