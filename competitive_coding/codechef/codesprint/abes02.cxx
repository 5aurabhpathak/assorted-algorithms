#include <cstdio>
#include <algorithm>
using namespace std;

int main()
{
	int t;
	scanf("%d", &t);
	long n, *a;
	while (t--) {
		scanf("%ld", &n);
		a = new long[n];
		for (long i = 0l; i < n; ++i) scanf("%ld", a+i);
		sort(a, a+n);
		for (long i = 0, j = n-1; i <= j; ++i, --j) {
			if (i == j) printf("%ld", a[i]);
			else printf("%ld %ld ", a[i], a[j]);
		}
		printf("\n");
		delete [] a;
	}
}
