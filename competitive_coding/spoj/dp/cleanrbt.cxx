#include <cstdio>
#include <set>
#include <unordered_map>
#include <utility>
using namespace std;

struct Vertex
{
	int x, y, dist;
	struct Compare
	{
		bool operator()(const Vertex &v1, const Vertex &v2) const
		{
			const static less<pair<int, int>> l;
			return l(make_pair(v1.x, v1.y), make_pair(v2.x, v2.y));
		}
	};
	Vertex(int x, int y) : x(x), y(y), dist(0) {}
	Vertex(int x, int y, int d) : x(x), y(y), dist(d) {}
};

class priority_queue : private set<Vertex, Vertex::Compare>
{
	public:
		using set<Vertex, Vertex::Compare>::emplace;
		using set<Vertex, Vertex::Compare>::empty;
		Vertex pop()
		{
			int min = 10000;
			iterator v;
			for (auto it = begin(); it != end(); it++)
				if (it->dist < min) {
					min = it->dist;
					v = it;
				}
			erase(v);
			return *v;
		}
};

int w, h;
set<pair<int,int>> dirty, obs;
unordered_map<int, unordered_map<int, unordered_map<int, int>>> dp;
unordered_map<int, unordered_map<int, unordered_map<int, unordered_map<int, int>>>> dist;

int solve(const pair<int, int> &, int);
bool solve();
int main()
{
	char c;
	pair<int, int> rb;
	scanf("%d%d", &w, &h);
	while (w && h) {
		dist.clear(), dp.clear(), dirty.clear(), obs.clear();
		for (int i = 0; i < h; i++)
			for (int j = 0; j < w; j++) {
				scanf(" %c", &c);
				switch (c) {
					case '.': break;
					case 'x': obs.emplace(j, i);
						  break;
					case 'o': rb.first = j;
						  rb.second = i;
					case '*': dirty.emplace(j, i);
				}
			}
		if (solve()) {
			dirty.erase(rb);
			printf("%d\n", solve(rb, 0));
		}
		else printf("-1\n");
		scanf("%d%d", &w, &h);
	}
}

//the pathfinder
int solve(const pair<int, int> &o, int mask)
{
	if (dp[mask][o.second][o.first]) return dp[mask][o.second][o.first];
	if (mask == (1<<dirty.size())-1) return 0;
	int &d = dp[mask][o.second][o.first] = 10000, i = 0, m;
	for (auto it = dirty.begin(); it != dirty.end(); i++, it++)
		if(!(mask & 1<<i) && (m = dist[o.second][o.first][it->second][it->first] + solve(*it, mask|1<<i)) < d) d = m;
	return d;
}

//all pair shortest path using bfs. No need for floyd-warshall
bool solve()
{
	for (auto it = dirty.begin(); it != dirty.end(); it++) {
		auto copy = set<pair<int,int>>(it, dirty.end());
		bool visited[100][100]{};
		priority_queue pq;
		pq.emplace(it->first, it->second);
		while (!pq.empty() && !copy.empty()) {
			auto v = pq.pop();
			visited[v.x][v.y] = true;
			auto it1 = copy.find(make_pair(v.x, v.y));
			if (it1 != copy.end()) {
				dist[it->second][it->first][v.y][v.x] = dist[v.y][v.x][it->second][it->first] = v.dist;
				copy.erase(*it1);
			}
			if (v.x+1 < w && !visited[v.x+1][v.y] && !obs.count(make_pair(v.x+1, v.y))) pq.emplace(v.x+1, v.y, v.dist+1);
			if (v.x-1 > -1 && !visited[v.x-1][v.y] && !obs.count(make_pair(v.x-1, v.y))) pq.emplace(v.x-1, v.y, v.dist+1);
			if (v.y+1 < h && !visited[v.x][v.y+1] && !obs.count(make_pair(v.x, v.y+1))) pq.emplace(v.x, v.y+1, v.dist+1);
			if (v.y-1 > -1 && !visited[v.x][v.y-1] && !obs.count(make_pair(v.x, v.y-1))) pq.emplace(v.x, v.y-1, v.dist+1);
		}
		if (!copy.empty()) return false;
	}
	return true;
}
