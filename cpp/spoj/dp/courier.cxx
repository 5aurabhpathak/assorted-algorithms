#include <cstdio>
#include <cstring>
#include <utility>
using namespace std;

int n, k, b, g[101][101], dp[101][4096];
pair<int, int> p[12];

void floyd_warshall();
int solve(int, int);
int main()
{
	int t, m, x, y, z;
	scanf("%d", &t);
	while (t--) {
		memset(dp, 0, sizeof dp);
		scanf("%d%d%d", &n, &m, &b);
		for (int i = 1; i <= n; i++) {
			for (int j = 1; j < i; j++) g[i][j] = g[j][i] = 10001;
			g[i][i] = 0;
		}
		for (int i = 0; i < m; i++) {
			scanf("%d%d%d", &x, &y, &z);
			if (g[x][y] > z) g[x][y] = g[y][x] = z;
		}
		floyd_warshall();
		k = 0;
		scanf("%d", &m);
		for (int i = 0; i < m; i++) {
			scanf("%d%d%d", &x, &y, &z);
			for (int j = 0; j < z; j++, k++) p[k] = make_pair(x,y);
		}
		printf("%d\n", solve(b, 0));
	}
}

void floyd_warshall()
{
	int t;
	for (int k = 1; k <= n; k++)
		for (int i = 1; i <= n; i++)
			for (int j = 1; j <= n; j++)
				if ((t = g[i][k] + g[k][j]) < g[i][j]) g[i][j] = t;
}

int solve(int v, int mask)
{
	if (dp[v][mask]) return dp[v][mask];
	if (mask == (1<<k)-1) return dp[v][mask] = g[v][b];
	int &res = dp[v][mask] = 10001, t;
	for (int i = 0; i < k; i++)
		if (!(mask & 1<<i) && (t = g[v][p[i].first] + g[p[i].first][p[i].second] + solve(p[i].second, mask|1<<i)) < res) res = t;
	return res;
}
