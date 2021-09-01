#include <iostream>
#include <string>
using namespace std;

string findlcs(const string &, const string &);
int main()
{
	string a, b;
	while (cin >> a >> b) {
		string lcs = findlcs(a, b);
		string ans;
		int i = 0, j = 0;
		for (int k = 0; k < lcs.size(); k++) {
			while (a[i] != lcs[k]) ans += a[i++];
			while (b[j] != lcs[k]) ans += b[j++];
			ans += lcs[k];
			i++;
			j++;
		}
		ans += a.substr(i) + b.substr(j);
		cout << ans << endl;
	}
}

string findlcs(const string &a, const string &b)
{
	string **dp = new string*[a.size()+1];
	for (int i = 0; i <= a.size(); i++)
		dp[i] = new string[b.size()+1]{};
	for (int i = 1; i <= a.size(); i++)
		for (int j = 1; j <= b.size(); j++)
			dp[i][j] = (a[i-1] == b[j-1]) ? dp[i-1][j-1] + b[j-1]: (dp[i-1][j].size() < dp[i][j-1].size()) ? dp[i][j-1]: dp[i-1][j];
	string ans(dp[a.size()][b.size()]);
	delete [] dp;
	return ans;
}
