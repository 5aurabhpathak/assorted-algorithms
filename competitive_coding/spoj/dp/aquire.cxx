#include <cstdio>
#include <utility>
#include <vector>
#include <algorithm>
using namespace std;

long long price(const vector<pair<long long, long long>>, vector<pair<long long, long long>> &);
void add(vector<pair<long long, long long>> &, long long, long long);
inline long long query(const vector<pair<long long, long long>> &, long long);
int main()
{
	long long n;
	scanf("%lld", &n);
	vector<pair<long long, long long>> p, q;
	for (long long i = 0; i < n; i++) {
		long long w, l;
		scanf("%lld%lld", &w, &l);
		p.emplace_back(w, l);
	}
	sort(p.begin(), p.end());
	auto it = p.begin();
	while(it != p.end()) {
		while ((!q.empty()) && q.back().second <= it->second)
			q.pop_back();
		q.push_back(*it++);
	}

	vector<pair<long long, long long>> l;
	add(l, q[0].second, 0);
	printf("%lld\n", price(q, l));
}

long long price(const vector<pair<long long, long long>> q, vector<pair<long long, long long>> &l)
{
	long long cost;
	for (long long i = 0; i < q.size(); i++) {
		cost = query(l, q[i].first);
		if (i < q.size()-1)
			add(l, q[i+1].second, cost);
	}
	return cost;
}

long long i = -1ll;
void add(vector<pair<long long, long long>> &l, long long m, long long c)
{
	while (l.size() > 1 && (l[l.size()-2].first - m) * (l.back().second - l[l.size()-2].second) >= (c - l[l.size()-2].second) * (l[l.size()-2].first - l.back().first)) {
		if (i == l.size()-1) i = -1;
		l.pop_back();
	}
	l.push_back(pair<long long, long long>(m, c));
	if (i == -1) i = l.size()-1;
}

long long query(const vector<pair<long long, long long>> &l, long long x)
{
	long long res = l[i].first * x + l[i].second, next;
	while((++i != l.size()) && (res >= (next = l[i].first * x + l[i].second))) res = next;
	--i;
	return res;
}
