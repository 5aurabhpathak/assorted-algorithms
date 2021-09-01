//http://scicomp.stackexchange.com/questions/812/how-to-implement-a-dynamic-programming-solution-to-the-2d-bitonic-euclidean-trav
//Can be made faster!
#include <cfloat>
#include <cmath>
#include <cstdio>
#include <utility>
using namespace std;

int main()
{
	int t;
	pair<long, long> a[1000];
	double d[1000][1000], dp[1000], m;
	scanf("%d", &t);
	for (int i = 0; i < t; i++) {
		scanf("%ld%ld", &a[i].first, &a[i].second);
		for (int j = 0; j < i; j++)
			d[i][j] = d[j][i] = sqrt(pow(a[j].second - a[i].second, 2) + pow(a[j].first - a[i].first, 2));
		d[i][i] = 0.0;
	}
	dp[0] = 0.0;
	dp[1] = d[0][1];
	for (int k = 2; k < t; k++) {
		dp[k] = DBL_MAX;
		for (int i = 0; i < k-1; i++) {
			m = d[k][i] + dp[i+1];
			for (int j = i+1; j < k-1; j++) m += d[j][j+1];
			if (m < dp[k]) dp[k] = m;
		}
	}
	printf ("%.2f\n", dp[t-1] + d[t-1][t-2]);
}
