#include <climits>
#include <cmath>
#include <cstdio>
#include <memory>
using namespace std;

struct Out
{
	int maxup, res;
	Out(int x, int y) : maxup(x), res(y) {}
	Out() : maxup(0), res(0) {}
};

int n, a[20][20];
shared_ptr<Out> dp[20][20];

int main()
{
	int t, T, time, maxupr, maxupd;
	shared_ptr<Out> r, d;
	scanf("%d", &t);
	while (t--) {
		scanf("%d%d", &n, &T);
		for (int i = 0; i < n; i++)
			for (int j = 0; j < n; j++) scanf("%d", *(a+i)+j);
		for (int i = n-1; i >= 0; i--)
			for (int j = n-1; j >=0; j--) {
				if (i == n-1 && j == n-1) {
					dp[i][j] = shared_ptr<Out>(new Out());
					continue;
				}
				maxupr = maxupd = INT_MAX;
				if (j+1 < n) {
					int rdiff = a[i][j+1]-a[i][j];
					maxupr = (rdiff > 0 && rdiff > dp[i][j+1]->maxup) ? rdiff : dp[i][j+1]->maxup;
					r = shared_ptr<Out>(new Out(maxupr, abs(rdiff)+dp[i][j+1]->res));
				}
				if (i+1 < n) {
					int ddiff = a[i+1][j]-a[i][j];
					maxupd = (ddiff > 0 && ddiff > dp[i+1][j]->maxup) ? ddiff : dp[i+1][j]->maxup;
					d = shared_ptr<Out>(new Out(maxupd, abs(ddiff)+dp[i+1][j]->res));
				}
				if (maxupr < maxupd) dp[i][j] = r;
				else if (maxupr > maxupd) dp[i][j] = d;
				else dp[i][j] = r->res < d->res? r : d;
			}
		if ((time = a[0][0] + dp[0][0]->res) < T) printf("YES : %d %d\n", a[0][0]>dp[0][0]->maxup ? a[0][0] : dp[0][0]->maxup , T-time);
		else printf("NO\n");
	}
}
