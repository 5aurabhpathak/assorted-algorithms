#include <cstdio>
using namespace std;

int dp[12][12][12][32]{};
bool done[12][12][12][32]{};
const int MOD(11380);

int solve(int, int, int, int);
int main()
{
	int t = 10;
	while (t--) {
		int w, x, y, z;
		scanf("%d%d%d%d", &w, &x, &y, &z);
		printf("%d\n", solve(w, x, y, z));
	}
}

int solve(int c, int s, int p, int d)
{
	if (done[c][s][p][d]) return dp[c][s][p][d];
	done[c][s][p][d] = true;
	if (!c && !s && !p)
		if (!d) return dp[c][s][p][d] = 1;
		else return 0;
	if (!d) return 0;
	if (d > c+s+p) return 0;
	int res = 0;
	for (int c1 = 0; c1 <= c; c1++)
		for (int s1 = 0; s1 <= s; s1++)
			for (int p1 = 0; p1 <= p; p1++)
				for (int d1 = 0; d1 < d; d1++) {
					int m, n;
					if (d1 == d-1) {
						m = 0;
						n = d;
					}
					else m = n = d;
					for (int d2 = m; d2 <= n; d2++) {
						if (c1 < c)
							res += solve(c1, s1, p1, d1) * solve(c-c1-1, s-s1, p-p1, d2);
						if (s1 < s && !c1)
							res += solve(0, s1, p1, d1) * solve(c, s-s1-1, p-p1, d2);
						if (p1 < p && !c1 && !s1)
							res += solve(0, 0, p1, d1) * solve(c, s, p-p1-1, d2);
						res %= MOD;
					}
				}
		return dp[c][s][p][d] = res;
}
