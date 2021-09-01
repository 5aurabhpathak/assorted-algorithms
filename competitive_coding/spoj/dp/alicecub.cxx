#include <algorithm>
#include <bitset>
#include <climits>
#include <iostream>
#include <queue>
#include <string>
#include <vector>
using namespace std;

struct Vertex
{
	bitset<16> b;
	int dist;
	Vertex(const char *c) : b(bitset<16>(c)), dist(0) {}
};

vector<Vertex> bfs();
vector<Vertex> neighbours(Vertex &, vector<Vertex> &);
int main()
{
	int t, i = 1;
	bitset<16> b;
	string s;
	vector<Vertex> v(bfs());
	cin >> t;
	cin.get();
	while (t--) {
		do getline(cin, s);
		while (s == "");
		s.erase(remove(s.begin(), s.end(), ' '), s.end());
		b = bitset<16>(s);
		auto pred = [&b](Vertex &a)->bool{ return a.b == b; };
		auto d = find_if(v.begin(), v.end(), pred);
		if (d != v.end()) cout << "Case #" << i++ << ": " << d->dist;
		else cout << "Case #" << i++ << ": more";
		cout << endl;
	}
}

vector<Vertex> bfs()
{
	vector<Vertex> v;
	auto comp = [](Vertex &a, Vertex &b)->bool{ return a.dist > b.dist; };
	priority_queue<Vertex, vector<Vertex>, decltype(comp)> pq(comp);
	pq.push("0000000011111111");
	auto a = pq.top();
	while (a.dist < 4) {
		v.push_back(a);
		pq.pop();
		for (Vertex n: neighbours(a, v)) {
			n.dist = a.dist + 1;
			pq.push(n);
		}
		a = pq.top();
	}
	return v;
}

vector<Vertex> neighbours(Vertex &v, vector<Vertex> &visited)
{
	vector<Vertex> n;
	static const int a[16][4]{{2,3,5,9}, {1,4,6,10}, {1,4,7,11}, {2,3,8,12},
		{1,6,7,13}, {2,5,8,14}, {3,5,8,15}, {4,6,7,16},
		{1,10,11,13}, {2,9,12,14}, {3,9,12,15}, {4,10,11,16},
		{5,9,14,15}, {6,10,13,16}, {7,11,13,16}, {8,12,14,15}};
	for (int i = 0; i < 16; i++)
		for (int j = 0; j < 4; j++)
			if (a[i][j] > i+1 && v.b[i] != v.b[a[i][j]-1]) {
				Vertex newn(v);
				newn.b[i].flip();
				newn.b[a[i][j]-1].flip();
				newn.dist = INT_MAX;
				auto comp = [&newn](Vertex &x)->bool{ return x.b == newn.b; };
				auto k = find_if(visited.begin(), visited.end(), comp);
				if (k == visited.end()) n.push_back(newn);
			}
	return n;
}
