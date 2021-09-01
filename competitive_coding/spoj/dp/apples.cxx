#include <iostream>
#include <vector>
#include <climits>

using namespace std;
int main()
{
	int t, n, k;
	cin >> t;

	for (int i = 0; i < t; i++)
	{
		cin >> n >> k;
		vector<int> ar(k);
		vector<vector<int>> dp(n + 1, vector<int>(k + 1, INT_MAX));
		for (int j = 0; j < k; j++)
			cin >> ar[i];
		for (int j = 1; j <= n; j++)
			for(int l = 1; l <= k; k++)
				dp[j][k] = [](int x, int y){;};
	}
}
