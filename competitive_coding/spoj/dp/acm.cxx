#include <iostream>
#include <string>
#include <cctype>
#include <vector>
#include <algorithm>
using namespace std;

long num(string, vector<string>, int, int, long **);
long num2(string, string, long **);
vector<string> getwords(vector < string >);
int main()
{
	int n;
	cin >> n;
	while (n)
	{
		vector < string > a(n);
		for (int i = 0; i < n; i++)
			cin >> a[i];
		string abvr;
		vector <string> words;
		cin >> abvr;
		words = getwords(a);
		while (abvr + ' ' + words[0] != "LAST CASE")
		{
			long **dp = new long *[words.size()];
			for (int i = 0; i < words.size(); i++)
				dp[i] = new long[abvr.size()]{};
			if (int c = num(abvr, words, abvr.size(), words.size(), dp))
				cout << abvr << " can be formed in " << c << " ways" << endl;
			else
				cout << abvr << " is not a valid abbreviation" << endl;
			for (int i = 0; i < words.size(); i++)
				delete [] dp[i];
			delete[]dp;
			cin >> abvr;
			words = getwords(a);
		}
		cin >> n;
	}
}

long num(string abvr, vector<string> words, int m, int n, long **dp)
{
	//cout << "numcall:\tm: " << m << "\tn: " << n << endl;
	if (dp[n-1][m-1]) return dp[n-1][m-1];
	if (n == 1) {
		string x = abvr.substr(0,m);
		long ** dp2 = new long*[x.size()];
		for (int i = 0; i < x.size(); i++)
			dp2[i] = new long[words[0].size()]{};
		dp[0][m-1] = num2(abvr.substr(0,m), words[0], dp2);
		for (int i = 0; i < x.size(); i++)
			delete [] dp2[i];
		delete [] dp2;
		//cout << "numreturn:\tm: " << m << "\tn: " << n << "\tcount :" << dp[0][m-1] << endl;
		return dp[0][m-1];
	}
	long count = 0l;
	for(int i = n - 1; i < m; i++) {
		string x = abvr.substr(i,m-i);
		long ** dp2 = new long*[x.size()];
		for (int j = 0; j < x.size(); j++)
			dp2[j] = new long[words[n-1].size()]{};
		count += num(abvr, words, i, n - 1, dp) * num2(x, words[n-1], dp2);
		for (int j = 0; j < x.size(); j++)
			delete [] dp2[j];
		delete [] dp2;
	}
	//cout << "numreturn:\tm: " << m << "\tn: " << n << "\tcount :" << count << endl;
	return dp[n-1][m-1] = count;
}

long num2(string abvr, string word, long **dp)
{
	//cout << "num2call:\tm: " << abvr.size() << "\tn: " << word.size() << endl;
	if (abvr.size() > word.size()) return 0l;
	int ow = word.size()-1;
	if (dp[abvr.size()-1][ow]) return dp[abvr.size()-1][ow];
	long count = 0l;
	int i;
	while ((i = word.find_last_of(tolower(abvr[abvr.size()-1]))) != string::npos) {
		word = word.substr(0, i);
		if (abvr.size() == 1) count++;
		else count += num2(abvr.substr(0, abvr.size()-1), word, dp);
	}
	//cout << "num2return:\tm: " << abvr.size() << "\tn: " << word.size() << "\tcount: " << count << endl;
	return dp[abvr.size()-1][ow] = count;
}

vector<string> getwords(vector < string > a)
{
	vector<string> out;
	string token;
	while (cin.get() != '\n') {
		cin >> token;
		if (find(a.begin(), a.end(), token) == a.end())
			out.push_back(token);
	}
	return out;
}
