#include <string>
#include <cstring>
#include <iostream>
#include <algorithm>
using namespace std;

int dp[6100][6100];

int num(const string &, int, int);
int main()
{
	int t;
	cin >> t;
	string s;
	while (cin >> s) {
		memset(dp, 0, sizeof(dp));
		cout << num(s, 0, s.size()) << endl;
	}
}

int num(const string &s, int b, int e)
{
	if (b >= e-1) return 0;
	if (dp[b][e-1]) return dp[b][e-1];
	return dp[b][e-1] = (s[b] == s[e-1]) ? num(s, b+1, e-1) : (1 + min(num(s, b, e-1), num(s, b+1, e)));
}
