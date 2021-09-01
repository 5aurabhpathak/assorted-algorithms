#include <iostream>
#include <algorithm>
#include <cstring>
using namespace std;

int r, c, k;
bool g[3000][3000];

bool check_in(int a, int b, int c, int d)
{
	for (int i = a; i < c; ++i)
		for (int j = b; j < d; ++j)
			if (g[i][j]) return false;
	return true;
}

int solve()
{
	int maxsize = min(r, c), count = r * c - k;
	for (int i = 0; i < r-1; ++i)
		for (int j = 0; j < c-1; ++j)
			for (int s = 2; s <= maxsize; ++s)
				if (!g[i][j] && i+s <= r && j+s <= c) {
					if (check_in(i+s-1, j, i+s, j+s) && check_in(i, j+s-1, i+s, j+s)) count++;
					else break;
				}
	return count;
}

int main()
{
	ios_base::sync_with_stdio(false);
	int t;
	cin >> t;
	for (int i = 1; i <= t; ++i) {
		cin >> r >> c >> k;
		memset(g, 0, sizeof g);
		for (int j = 0; j < k; ++j) {
			int ri, ci;
			cin >> ri >> ci;
			g[ri][ci] = true;
		}
		cout << "Case #" << i << ": " << solve() << endl;
	}
}
