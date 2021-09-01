#include <algorithm>
#include <cstdio>
#include <cmath>
using namespace std;

int main()
{
	int n, m, k;
	scanf("%d%d", &n, &m);
	long *b = new long[n], *c = new long[m], l, min, sum = 0l;
	bool *d = new bool[m]{};
	for (int i = 0; i < n; ++i) scanf("%ld", b+i);
	for (int i = 0; i < m; ++i) scanf("%ld", c+i);
	sort(b, b+n);
	sort(c, c+m);
	for (int i = 0; i < n; ++i) {
		min = 1000000l;
		for (int j = 0; j < m; ++j)
			if (!d[j] && (l = abs(b[i]-c[j])) < min) min = l, k = j;
		d[k] = true;
		sum += min;
	}
	printf("%ld\n", sum);
}
