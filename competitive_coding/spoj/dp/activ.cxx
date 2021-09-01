#include <cstdio>
#include <utility>
#include <algorithm>
using namespace std;

auto comp = [](auto p1, auto p2)->bool {return p1.second < p2.second;};

long subsets_bu(pair<long, long> p[], unsigned n);
int main()
{
	unsigned n;
	scanf("%u", &n);
	while (n != -1u) {
		pair<long, long> * p = new pair<long, long>[n];
		for (unsigned i = 0u; i < n ; i++) {
			long s, e;
			scanf("%ld%ld", &s, &e);
			p[i] = pair<long, long>(s, e);
		}
		sort(p, p+n, comp);
		printf("%08ld\n", subsets_bu(p, n));
		delete [] p;
		scanf("%u", &n);
	}
}

long subsets_bu(pair<long, long> *p, unsigned n)
{
	long *dp = new long [n]{1l};
	pair<long, long> *it = nullptr;
	for (unsigned i = 1u; i < n; i++)
		dp[i] = ((it = upper_bound(p, p+i, pair<long, long>(0l, p[i].first), comp)-1)== p-1? 1l + dp[i-1]: dp[it-p] + dp[i-1] + 1l) % 100000000l;
	long ans = dp[n-1u];
	delete [] dp;
	return ans;
}
