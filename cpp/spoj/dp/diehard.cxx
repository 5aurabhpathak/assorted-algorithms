#include <algorithm>
#include <cstdio>
using namespace std;

int dp[10004][1008][3]{};

int solve(int, int, int);
int main()
{
	int t, h, a;
	scanf("%d", &t);
	while (t--) {
		scanf("%d%d", &h, &a);
		printf("%d\n", solve(h, a, 0));
	}
}

int solve(int h, int a, int p)
{
	if (dp[h][a][p]) return dp[h][a][p];
	if (!p && h > 0 && a > 0) return dp[h][a][p] = 1 + max(solve(h+3, a+2, 1), solve(h+3, a+2, 2));
	if (p == 1 && h > 20 && a > 0 ) return dp[h][a][p] = 1 + max(solve(h-20, a+5, 0), solve(h-20, a+5, 2));
	if (p == 2 && h > 5 && a > 10) return dp[h][a][p] = 1 + max(solve(h-5, a-10, 0), solve(h-5, a-10, 1));
	return 0;
}
