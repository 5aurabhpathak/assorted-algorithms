#include <algorithm>
#include <cstdio>
#include <numeric>
using namespace std;

int main()
{
	int m, n, a[10000], b[10000];
	scanf("%d", &m);
	while (m) {
		for (int i = 0; i < m; i++)
			scanf("%d", a+i);
		scanf("%d", &n);
		for (int i = 0; i < n; i++)
			scanf("%d", b+i);
		int j = m < n? m : n, ai = 0, bi = 0;
		long sum = 0l, suma, sumb;
		for (int i = 0; i < j; i++) {
			int *s;
			if (j == m) {
				s = lower_bound(b+bi, b+n, a[i]);
				if (*s == a[i]) {
					sumb = accumulate(b+bi, s, 0l);
					suma = accumulate(a+ai, a+i, 0l);
					sum += (suma > sumb? suma : sumb) + a[i];
					bi = s-b+1;
					ai = i+1;
				}
			}
			else {
				s = lower_bound(a+ai, a+m, b[i]);
				if (*s == b[i]) {
					sumb = accumulate(b+bi, b+i, 0l);
					suma = accumulate(a+ai, s, 0l);
					sum += (suma > sumb? suma : sumb) + b[i];
					bi = i+1;
					ai = s-a+1;
				}
			}
		}
		sumb = accumulate(b+bi, b+n, 0);
		suma = accumulate(a+ai, a+m, 0);
		printf("%ld\n", suma > sumb? sum+suma: sum+sumb);
		scanf("%d", &m);
	}
}
