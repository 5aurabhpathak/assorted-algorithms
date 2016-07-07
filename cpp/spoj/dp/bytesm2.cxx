#include <cstdio>
#include <cstring>
using namespace std;

int a[100][100], h, w, dp[101][102];

int solve();
int solve(int, int);
int main()
{
	int t;
	scanf("%d", &t);
	while (t--) {
		scanf("%d%d", &h, &w);
		for (int i = 0; i < h; i++)
			for (int j = 0; j < w; j++) scanf("%d", *(a+i)+j);
		memset(dp, -1, sizeof dp);
		printf("%d\n", solve());
	}
}

int solve()
{
	int max = 0, m;
	for (int i = 0; i < w; i++)
		if ((m = solve(0, i)) > max) max = m;
	return max;
}

int solve(int h, int w)
{
	if (dp[h][w+1] != -1) return dp[h][w+1];
	if (h == ::h || w == ::w || w == -1) return dp[h][w+1] = 0;
	int m1 = solve(h+1, w-1), m2 = solve(h+1, w), m3 = solve(h+1, w+1);
	return dp[h][w+1] = a[h][w] + (m1>m2 ? m1>m3 ? m1 : m3 : m2>m3? m2 : m3);
}
