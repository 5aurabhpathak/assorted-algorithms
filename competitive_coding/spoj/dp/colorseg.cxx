#include <cstdio>
using namespace std;

const long MOD = 1000003l;
long dp[51][51][51][51]{}, ways[51][51]{};
bool cp[101][101];

bool coprime(int, int);
void solve();
int main()
{
	int t, n, m;
	for (int i = 2; i <= 100; i++) {
		for (int j = 2; j < i; j++) cp[i][j] = cp[j][i] = coprime(i, j);
		cp[i][i] = false;
	}
	solve();
	scanf("%d", &t);
	for (int i = 1; i <= t; i++) {
		scanf("%d%d", &n, &m);
		printf("Case %d: %ld\n", i, ways[n][m]);
	}
}

bool coprime(int a, int b)
{
	int t;
	while (b) {
		t = b;
		b = a % b;
		a = t;
	}
	return a == 1;
}

void solve()
{
	for (int y = 1; y <= 50; y++) {
		ways[1][y] = y;
		for (int i = 1; i <= y; i++)
			for (int j = 1; j <= y; j++) ways[2][y] += dp[2][y][i][j] = 1l;
		for (int x = 3; x <= 50; x++) {
			for (int i = 1; i <= y; i++)
				for (int j = 1; j <= y; j++)
					for (int k = 1; k <=y; k++)
						if (cp[i+j][j+k] && (dp[x][y][j][k] += dp[x-1][y][i][j]) >= MOD) dp[x][y][j][k] -= MOD;
			for (int i = 1; i <= y; i++)
				for (int j = 1; j <= y; j++)
					if ((ways[x][y] += dp[x][y][i][j]) >= MOD) ways[x][y] -= MOD;
		}
	}
}
