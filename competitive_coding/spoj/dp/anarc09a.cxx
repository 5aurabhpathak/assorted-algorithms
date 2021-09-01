#include <cstdio>
#include <cstring>
using namespace std;

char s[2001];
int **dp;
int i = 1;

int solve(int, int);
void solve_dp();
void solve_linear();
int match(int, int);
int main()
{
	scanf("%s", s);
	while (s[0] != '-') {
		//solve_dp();
		solve_linear();
		scanf("%s", s);
	}
}

void solve_dp()
{
	int l = strlen(s);
	dp = new int*[l];
	for (int i = 0; i < l; i++) {
		dp[i] = new int[l];
		memset(dp[i], -1, l * sizeof (int));
	}
	printf("%d. %d\n", i++, solve(0, strlen(s)));
	for (int i = 0; i < l; i++) delete [] dp[i];
	delete [] dp;
}

int solve(int b, int e)
{
	if (dp[b][e-1] != -1) return dp[b][e-1];
	if (e <= b) return dp[b][e-1] = 0;
	if (e - b == 2) return dp[b][e-1] = match(b, e);
	int count = 2001;
	for (int i = b; i < e; i+=2) {
		int c = solve(b, i) + solve(i+1, e-1) + match(i, e);
		if (c < count) count = c;
	}
	return dp[b][e-1] = count;
}

int match(int b, int e)
{
		if (s[b] == '}') {
			if (s[e-1] == '}') return 1;
			return 2;
		}
		if (s[e-1] == '}') return 0;
		return 1;
}

void solve_linear()
{
	int co = 0, cc = 0, l = strlen(s);
	for (int i = 0; i < l; i++) {
		if (s[i] == '{') co++;
		else if (co) co--;
		else cc++;
	}
	printf("%d. %d\n", i++, co % 2 ? co/2+cc/2+2 : co/2+cc/2);
}
