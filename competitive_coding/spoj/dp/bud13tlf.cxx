#include <cstdio>
using namespace std;

int a[100];
const int MOD = 10007;

int solve(int, int);
int main()
{
	int t, n, w, c = 0;
	scanf("%d", &t);
	while (t--) {
		scanf("%d%d", &n, &w);
		for (int i = 0; i < n; i++) scanf("%d", a+i);
		printf("Case %d: %d\n", ++c, solve(n-1, w));
	}
}

int solve(int n, int w)
{
	if (!w) return 1;
	if (!n) return a[0] == w;
	int sum = 0;
	for (int i = 0; i < a[n]; i++) sum = (sum + solve(n-1, w-a[n]+i)) % MOD;
	return sum;
}
