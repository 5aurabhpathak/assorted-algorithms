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
	int n = read<int>(), k = read<int>(), j, *a = new int[n];
	long long *b = new long long[n], sum = 0ll;
	for (int i = 0; i < n; ++i) a[i] = read<int>();
	sort(a, a+n);
	b[0] = 0ll;
	for (int i = 1; i < n; ++i) {
		if (k <= a[i]) break;
		j = lower_bound(a, a+i, k-a[i])-a;
		if (i == j) b[i] = b[j-1] + 1;
		else b[i] = b[j] + (a[i] + a[j] < k);
		sum += b[i];
	}
	printf("%lld\n", sum);
}
