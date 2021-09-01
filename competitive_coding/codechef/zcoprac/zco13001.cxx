#include <algorithm>
#include <cstdio>
#include <numeric>
using namespace std;

template <typename T> T read();
int main()
{
	int n = read<int>(), *a = new int[n];
	long long *sum = new long long[n];
	sum[0] = 0ll;
	for (int i = 0; i < n; ++i) a[i] = read<int>();
	sort(a, a+n);
	for (int i = 1; i < n; ++i) sum[i] = sum[i-1] + i * (a[i] - a[i-1]);
	printf("%lld\n", accumulate(sum, sum+n, 0ll));
}

template <typename T>
T read()
{
	register T x = (T) 0;
	register char c = getchar_unlocked();
	while (c < 48 || c > 57) c = getchar_unlocked();
	while (c > 47 && c < 58) {
		x = (x << 1) + (x << 3) + (c & 15);
		c = getchar_unlocked();
	}
	return x;
}
