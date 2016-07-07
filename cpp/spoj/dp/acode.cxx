#include <iostream>
#include <string>
using namespace std;

long long num(string, long long *);
int main()
{
	string l;
	getline(cin, l);
	while (l != "0") {
		long long *dp = new long long[l.size()]{};
		cout << num(l, dp) << endl;
		delete [] dp;
		getline(cin, l);
	}
}

long long num(string l, long long *dp)
{
	if (!l.size()) return 1ll;
	if (dp[l.size()-1]) return dp[l.size()-1];
	if (l.size() == 1) return dp[l.size() -1] = 1ll;
	if (l[l.size()-1] == '0') return dp[l.size()-1] = num(l.substr(0, l.size()-2), dp);
	return dp[l.size()-1] = (stoi(l.substr(l.size()-2, l.size())) <= 26 && l[l.size()-2] != '0' ? num(l.substr(0, l.size()-1), dp) + num(l.substr(0, l.size()-2), dp) : num(l.substr(0, l.size()-1), dp));
}
