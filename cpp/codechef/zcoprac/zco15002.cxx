#include <algorithm>
#include <cstdio>
using namespace std;

template <typename T> T read()
{
	T x = 0;
	char c = getchar_unlocked();
	while (c < 48 || c > 57) c = getchar_unlocked();
	while (c > 47 && c < 58) {
		x = (x << 1) + (x << 3) + (c & 15);
		c = getchar_unlocked();
	}
	return x;
}

int main()
{
	long n = read<long>(), k = read<long>(), *a = new long[n], *b = new long[n], sum = 0;
	for (long i = 0; i < n; ++i) a[i] = read<long>();
	sort(a, a+n);
	b[0] = 0;
	for (long i = 1; i < n; ++i) {
		long j = lower_bound(a, a+i, a[i]-k) - a;
		if (j == i) b[i] = b[i-1] + 1;
		else if (a[i] - a[j] < k) b[i] = b[j];
		else b[i] = b[j] + 1;
		sum += b[i];
	}
	printf("%ld\n", sum);
}
