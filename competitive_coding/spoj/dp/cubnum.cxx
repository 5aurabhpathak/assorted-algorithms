#include <climits>
#include <cmath>
#include <cstdio>
using namespace std;

int dp[100000]{};

int solve(long);
int main()
{
	long n, i = 0;
	while (scanf("%ld", &n) != EOF) printf("Case #%ld: %d\n", ++i, solve(n));
}

int solve(long n)
{
	if (!n) return 0;
	if (dp[n-1]) return dp[n-1];
	int t, &m = dp[n-1] = INT_MAX;
	for (int i = 1; i <= cbrt(n); i++)
		if ((t = 1 + solve(n - pow(i, 3))) < m) m = t;
	return m;
}
