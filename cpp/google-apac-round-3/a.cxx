#include <iostream>
#include <algorithm>
#include <vector>
#include <cmath>
using namespace std;

int r, c, rs, cs, s;
double p, q;
char grid[20][20];

double solve(int rs, int cs, int s, vector<vector<int>> v, bool first)
{
	double left, right, up, down;
	double d = !first ? grid[rs][cs] == 'A'? pow(1-p, v[rs][cs]) * p : pow(1-q, v[rs][cs]) * q : 0.0;
	if (!s) return d;
	if (!first) v[rs][cs]++;
	//go left
	if (cs > 0) left = solve(rs, cs-1, s-1, v, false);
	if (cs < c-1) right = solve(rs, cs+1, s-1, v, false);
	if (rs > 0) up = solve(rs-1, cs, s-1, v, false);
	if (rs < r-1) down = solve(rs+1, cs, s-1, v, false);
	return d + max(max(max(right, left), down), up);
}

int main()
{
	ios_base::sync_with_stdio(false);
	cout.setf(ios_base::fixed, ios_base::floatfield);
	cout.precision(7);
	int t, i = 0;
	cin >> t;
	while (t--) {
		cin >> r >> c >> rs >> cs >> s >> p >> q;
		vector<vector<int>> v(r);
		for (int i = 0; i < r; ++i)
			for (int j = 0; j < c; ++j) {
				cin >> grid[i][j];
				v[i].push_back(0);
			}
		cout << "Case #" << ++i << ": " << solve(rs, cs, s, v, true) << endl;
	}
}
