#include <cstdio>
#include <memory>
#include <vector>
using namespace std;

struct Line
{
	long long m;
	long long p;
	Line(long long M, long long P) : m(M), p(P) {}
};
vector<unique_ptr<Line>> E;
long long a, b, c, n, it;
long long *dp;
long long *x;

void solve();
void add(long long, long long);
long long query(long long);
int main()
{
	int t;
	scanf("%d", &t);
	while(t--) {
		scanf("%lld", &n);
		scanf("%lld%lld%lld", &a, &b, &c);
		x = new long long[n+1];
		x[0] = 0l;
		for (long long i = 1; i <= n; i++) {
			scanf("%lld", x+i);
			x[i] += x[i-1];
		}
		solve();
		delete [] x;
	}
}

void solve()
{
	dp = new long long[n+1];
	dp[0] = 0ll;
	E.emplace_back(new Line(0, 0));
	it = 0;
	for (long long i = 1; i <= n; i++) {
		dp[i] = query(i) + a*x[i]*x[i] + b*x[i] + c;
		if (i < n) add(-2*a*x[i], dp[i] + a*x[i]*x[i] - b*x[i]);
	}
	printf("%lld\n", dp[n]);
	E.clear();
	delete [] dp;
}

void add(long long m, long long p)
{
	while (E.size()>1 && (E[E.size()-2]->m-E[E.size()-1]->m)*(p-E[E.size()-2]->p) <= (E[E.size()-2]->m-m)*(E[E.size()-1]->p-E[E.size()-2]->p)) {
		if (it == E.size()-1) it = -1;
		E.pop_back();
	}
	E.emplace_back(new Line(m, p));
	if (it == -1) it = E.size()-1;
}

long long query(long long i)
{
	long long res = x[i]*E[it]->m + E[it]->p, c;
	while (++it != E.size() && res <= (c = x[i]*E[it]->m + E[it]->p)) res = c;
	it--;
	return res;
}
