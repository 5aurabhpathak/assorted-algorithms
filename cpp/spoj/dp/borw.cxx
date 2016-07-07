#include <cstdio>
#include <cstring>
using namespace std;

long a[202];
int n, dp[202][202][202];

int solve(int, int, int);
int main()
{
	scanf("%d", &n);
	while (n != -1) {
		for (int i = 1; i <= n; i++) scanf("%ld", a+i);
		memset(dp, 0, sizeof dp);
		printf("%d\n", n-solve(1, 0, 0));
		scanf("%d", &n);
	}
}

int solve(int n, int i, int d)
{
	if (dp[n][i][d]) return dp[n][i][d];
	if (n > ::n) return 0;
	int x = !i || (a[n] > a[i]) ? 1+solve(n+1, n, d) : 0;
	int y = !d || (a[n] < a[d]) ? 1+solve(n+1, i, n) : 0;
	int z = solve(n+1, i, d);
	return dp[n][i][d] = x > y ? x > z? x : z : y > z? y : z;
}
