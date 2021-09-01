//O(2N + N^2) solution. Somehow, this was 0.02s slower than my earlier
//O(2N^2) solution. Maybe because their test cases do not incite asymptotic
//behaviour.
#include <cstdio>
using namespace std;

int main()
{
	int t, n, m, max, a[1000], dpi[1000], dpr[1000];
	scanf("%d", &t);
	while (t--) {
		max = 0;
		scanf("%d", &n);
		for (int i = 0; i < n; i++) scanf("%d", a+i);
		for (int i = 0; i < n; i++) {
			dpi[i] = dpr[n-1-i] = 1;
			for (int j = 0; j < i; j++) {
				if (a[i] > a[j] && (m = 1 + dpi[j]) > dpi[i]) dpi[i] = m;
				if (a[n-i-1] > a[n-j-1] && (m = 1 + dpr[n-1 -j]) > dpr[n-1-i]) dpr[n-1-i] = m;
			}
		}
		for (int i = 0; i < n; i++)
			if ((m = dpi[i]+dpr[i]-1) > max) max = m;
		printf("%d\n", max);
	}
}
