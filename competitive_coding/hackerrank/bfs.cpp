//bfs with adjacency lists
#include <algorithm>
#include <deque>
#include <iostream>
#include <iterator>
#include <unordered_set>
#include <vector>
using namespace std;

int main()
{
	int q, n, m, s;
	ios_base::sync_with_stdio(false);
	cin >> q;
	while (q--) {
		cin >> n >> m;
		vector<unordered_set<int>> g(n);
		for (int i = 0; i < m; ++i) {
			int u, v;
			cin >> u >> v;
			g[u-1].insert(v-1);
			g[v-1].insert(u-1);
		}
		cin >> s;
		deque<int> Q{s-1};
		vector<int> d(n);
		fill(d.begin(), d.end(), -1);
		bool *v = new bool[n]{};
		while (!Q.empty()) {
			int N = Q.front();
			Q.pop_front();
			if (v[N]) continue;
			v[N] = true;
			copy_if(g[N].begin(), g[N].end(), back_inserter(Q), [v, &d, N](int a)->bool{ if (!v[N]) d[a] = d[N] + 6; return !v[N]; });
		}
		int i = 0;
		copy_if(d.begin(), d.end(), ostream_iterator<int>(cout, " "), [&i, s](int x)->bool{ return ++i != s; });
		cout << endl;
		delete [] v;
	}
}
