#include <cstdio>
using namespace std;

int main()
{
	long n, h, pos = 0l, a[100000];
	int c;
	bool hasbox = false;
	scanf("%ld%ld", &n, &h);
	for (long i = 0; i < n; ++i) scanf("%ld", a+i);
	scanf("%d", &c);
	while (c) {
		switch (c) {
			case 1: if (pos > 0) --pos;
				break;
			case 2: if (pos < n-1) ++pos;
				break;
			case 3: if (!hasbox && a[pos]) --a[pos], hasbox = true;
				break;
			case 4: if (hasbox && a[pos] < h) ++a[pos], hasbox = false;
		}
		scanf("%d", &c);
	}
	for (long i = 0; i < n; ++i) printf("%ld ", a[i]);
	printf("\n");
}
