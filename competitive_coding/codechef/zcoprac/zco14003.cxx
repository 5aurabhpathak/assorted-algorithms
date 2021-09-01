#include <algorithm>
#include <cstdio>
using namespace std;

int main()
{
	long t;
	long long a[500000], m, k;
	scanf("%ld", &t);
	for (long i = 0; i < t; ++i) scanf("%lld", a+i);
	sort(a, a+t);
	m = a[0] * t;
	for (long i = 1; i < t; ++i)
		if ((k = a[i] * (t-i)) > m) m = k;
	printf("%lld\n", m);
}
