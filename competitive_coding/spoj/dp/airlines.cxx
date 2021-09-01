#include <iostream>
#include <vector>
#include <bitset>
#include <cstring>
using namespace std;

struct Pattern: public bitset<15>
{
	int length;
	vector<int> comp;
	Pattern() : length(0) {}
	bool compatwith(const Pattern *p) const
	{
		if ((*p & *this).any()) return false;
		return true;
	}
};

const long MOD(420047l);
long dp[32768][50][51];
vector<Pattern *> patterns;
int m;

long solve(long long, int);
long solve_large(long long, int);
long solve(int, long long, int);
void genpatterns(int);
vector<vector<long>> matmul(const vector<vector<long>> &, const vector<vector<long>> &);
vector<vector<long>> pow(const vector<vector<long>> &, long long);
int main()
{
	int k;
	long long n;
	int prevm = 0;
	while(cin >> m >> n >> k) {
		if (prevm != m) {
			memset(dp, -1, sizeof(dp));
			patterns = vector<Pattern *>();
			patterns.push_back(new Pattern());
			genpatterns(k);
		}
		if (n > 50) cout << solve_large(n,k) << endl;
		else cout << solve(n, k) << endl;
		prevm = m;
	}
}

void genpatterns(int k)
{
	for (int mm = 0; mm < m; mm++) {
		int l = patterns.size();
		for (int i = 0; i < l; i++) {
			patterns[i]->length++;
			if (patterns[i]->count() < k && (!mm || !(*patterns[i])[patterns[i]->length-2])) {
				Pattern *newp = new Pattern(*patterns[i]);
				(*newp)[newp->length-1] = true;
				patterns.push_back(newp);
			}
		}
	}
	for (int i = 0; i < patterns.size(); i++)
		for (int j = 0; j < patterns.size(); j++)
			if (patterns[i]->compatwith(patterns[j]))
				patterns[i]->comp.push_back(j);
}

long solve(long long n, int k)
{
	long res = 0l;
	for (int i = 0; i < patterns.size(); i++)
		res += solve(i, n-1ll, k-patterns[i]->count());
	return res % MOD;
}

long solve(int i, long long n, int k)
{
	if (dp[i][n][k] != -1) return dp[i][n][k];
	if (!k) return dp[i][n][k] = 1l;
	if (n * (m / 2 + m % 2) < k) return dp[i][n][k] = 0l; //heuristic
	long res = 0l;
	for (int j : patterns[i]->comp)
		if (n == 1ll) {
			if(k == patterns[j]->count()) res++;
		}
		else if (k >= patterns[j]->count()) res += solve(j, n-1ll, k-patterns[j]->count());
	return dp[i][n][k] = res % MOD;
}

long solve_large(long long n, int k)
{
	vector<vector<long>> v{vector<long>()};
	for (int i = 0; i < patterns.size(); i++)
		for (int j = 0; j <= k; j++)
			if (patterns[i]->count() == j) v[0].push_back(1);
			else v[0].push_back(0);
	int dim = patterns.size() * (k+1);
	vector<vector<long>> matrix(dim, vector<long>(dim));
	for (int i = 0; i < dim; i++)
		for (int j = 0; j < dim; j++)
			if (j%(k+1)+patterns[i/(k+1)]->count() == i%(k+1) && patterns[j/(k+1)]->compatwith(patterns[i/(k+1)])) matrix[j][i] = 1l;
			else matrix[j][i] = 0l;
	matrix = pow(matrix, n-1);
	v = matmul(v, matrix);
	long sum = 0l;
	for (auto it = v[0].begin() + k; it < v[0].end(); it += k+1)
		sum += *it;
	return sum % MOD;
}

vector<vector<long>> matmul(const vector<vector<long>> &mat1, const vector<vector<long>> &mat2)
{
	vector<vector<long>> res(mat1.size(), vector<long>(mat2[0].size()));
	for (int i = 0; i < mat1.size(); i++)
		for (int j = 0; j < mat2[0].size(); j++) {
			res[i][j] = 0;
			for (int k = 0; k < mat2.size(); k++)
				res[i][j] += (mat1[i][k] * mat2[k][j]) % MOD;
		}
	return res;
}

vector<vector<long>> pow(const vector<vector<long>> &mat, long long n)
{
	if (!n) {
		vector<vector<long>> res(mat.size(), vector<long>(mat[0].size()));
		for (int i = 0; i < mat.size(); i++)
			for (int j = 0; j < mat.size(); j++)
				if (i == j) res[i][j] = 1l;
				else res[i][j] = 0l;
		return res;
	}
	if (n == 1) return mat;
	if (n % 2) return matmul(mat, pow(matmul(mat, mat), n>>1));
	return pow(matmul(mat, mat), n>>1);
}
