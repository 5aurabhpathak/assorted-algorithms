#include <cstdio>
using namespace std;

int main()
{
	int t, i, dp[2001][3];
	char c;
	dp[0][0] = dp[0][1] = dp[0][2] = 0;
	scanf("%d", &t);
	getchar_unlocked();
	while (t--) {
		i = 0;
		c = getchar_unlocked();
		while (c != '\n') {
			++i;
			if (c == 'K') {
				dp[i][0] = dp[i-1][0] + 1;
				dp[i][1] = dp[i-1][1];
				dp[i][2] = dp[i-1][2] + dp[i-1][1];
			}
			else if (c == 'E') {
				dp[i][0] = dp[i-1][0];
				dp[i][1] = dp[i-1][1] + dp[i-1][0]; 
				dp[i][2] = dp[i-1][2];
			}
			else {
				dp[i][0] = dp[i-1][0];
				dp[i][1] = dp[i-1][1];
				dp[i][2] = dp[i-1][2];
			}
			c = getchar_unlocked();
		}
		printf("%d\n", dp[i][2]);
	}
}
