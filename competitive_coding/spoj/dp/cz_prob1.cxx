#include <cstdio>
#include <cstdlib>
#include <ctime>
using namespace std;

int sp2[500];

void populate_sp2();
bool isprime(int);
int modpow(int, int);
int main()
{
	int t, n, k;
	long dp[7994][4];
	srand(time(NULL));
	populate_sp2();
	for (int i = 0; i < 4; ++i) dp[0][i] = 1l;
	for (int i = 1; i < 7994; ++i) dp[i][0] = 0l;
	for (int i = 1; i <= 7993; ++i)
		for (int j = 1; j <= 3; ++j) dp[i][j] = dp[i][j-1] + (j<=i? dp[i-j][j] : 0);
	scanf("%d", &t);
	while (t--) {
		scanf("%d%d", &n, &k);
		printf("%ld\n", dp[sp2[n-1]][k]);
	}
}

void populate_sp2() //pythagorean prime
{
	int k;
	sp2[0] = 2;
	for (int i = 1, j = 0; i < 500; ++i) {
		while (!isprime(k = 4*++j+1));
		sp2[i] = k;
	}
}

bool isprime(int n) //fermat's little theorem -- max 50 witnesses
{
	int a;
	for (int i = 0; i < (n>50 ? 50 : n); ++i) {
		a = rand() % (n-1) + 1;
		if (modpow(a, n-1) != 1) return false;
	}
	return true;
}

int modpow(int a, int n) //recursive gave TLE. iterative AC!
{
	int res = 1, p = n + 1;
	while (n) {
		if (n & 1) res = (res * a) % p;
		n >>= 1;
		a = (a*a) % p;
	}
	return res;
}
