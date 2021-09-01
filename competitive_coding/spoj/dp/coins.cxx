#include <algorithm>
#include <cstdio>
#include <map>
using namespace std;

map<long, long long> dp;

long long solve(long);
int main()
{
	long n;
	while (scanf("%ld", &n) != EOF) {
		printf("%lld\n", solve(n));
		dp.clear();
	}
}

long long solve(long n)
{
	if (!n) return 0ll;
	if (n == 1l) return 1ll;
	if (dp[n]) return dp[n];
	return dp[n] = max(solve(n/2l)+solve(n/3l)+solve(n/4l), (long long) n);
}
