#include <cmath>
#include <cstdio>
#include <vector>
#include <utility>
using namespace std;

int main()
{
	int t, n, tmp, sum;
	bool flag;
	scanf("%d", &t);
	while (t--) {
		sum = 0;
		flag = false;
		scanf("%d", &n);
		vector <pair<int, int>> s;
		pair <int, int> in;
		for (int i = 0; i < n; ++i)
			for (int j = 0; j < n; ++j) {
				scanf("%d", &tmp);
				switch (tmp) {
					case 1: s.emplace_back(i, j);
						break;
					case 5: in = make_pair(i, j);
						flag = true;
				}
			}
		if (!flag) {
			printf("-1\n");
			continue;
		}
		for (auto &p : s) sum += abs(p.first - in.first) + abs(p.second - in.second);
		printf("%d\n", sum);
	}
}
