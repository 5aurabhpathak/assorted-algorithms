#include <cstdio>
using namespace std;

int main()
{
	int t, n, m, c;
	long long count;
	scanf("%d", &t);
	while (t--) {
		count = 0ll;
		scanf("%d%d%d", &n, &m, &c);
		int tmp = n > c ? c : n;
		for (int i = 1; i <= tmp; ++i)
			if (!(c % i) && (c / i) <= m) count++;
		printf("%lld\n", count);
	}
}
