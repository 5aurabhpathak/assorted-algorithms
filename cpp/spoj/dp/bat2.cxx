#include <cstdio>
#include <cstring>
using namespace std;

int a[100], n, dp[100][100][101];

int solve(int, int , int);
int main()
{
	int t;
	scanf("%d", &t);
	while (t--) {
		scanf("%d", &n);
		for (int i = 0; i < n; i++) scanf("%d", a+i);
		memset(dp, 0, sizeof dp);
		printf("%d\n", solve(0, 0, 101));
	}
}

int solve(int n, int i, int d)
{
	if (dp[n][i][d]) return dp[n][i][d];
	if (n == ::n) return 0;
	int x = a[n] > i ? 1+solve(n+1, a[n], d) : 0, y = a[n] < d ? 1+solve(n+1, i, a[n]) : 0, z = solve(n+1, i, d);
	return dp[n][i][d] = x > y ? x > z? x : z : y > z? y : z;
}
