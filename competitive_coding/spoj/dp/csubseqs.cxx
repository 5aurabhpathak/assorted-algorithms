/*Tricky problem! Extended this paper's solution for two strings to four string case. AC!
 * http://compalg.inf.elte.hu/~tony/Kutatas/PerfectArrays/Elzinga-AlgorithmsSubsequenceCombinatorics.pdf*/
#include <cstdio>
#include <cstring>
using namespace std;

int main()
{
	char A[51], B[51], C[51], D[51];
	int la[51][26], lb[51][26], lc[51][26], ld[51][26];
	static long long dp[51][51][51][51];
	scanf("%s%s%s%s", A, B, C, D);
	int a = strlen(A), b = strlen(B), c = strlen(C), d = strlen(D), ia, ib, ic, id;
	memset(la[0], 0, sizeof la[0]), memset(lb[0], 0, sizeof lb[0]), memset(lc[0], 0, sizeof lc[0]), memset(ld[0], 0, sizeof ld[0]);
	for (int i = 0; i < 26; i++) {
		for (int j = 1; j <= a; j++) la[j][i] = A[j-1]-'a'!=i ? la[j-1][i] : j;
		for (int j = 1; j <= b; j++) lb[j][i] = B[j-1]-'a'!=i ? lb[j-1][i] : j;
		for (int j = 1; j <= c; j++) lc[j][i] = C[j-1]-'a'!=i ? lc[j-1][i] : j;
		for (int j = 1; j <= d; j++) ld[j][i] = D[j-1]-'a'!=i ? ld[j-1][i] : j;
	}
	for (int i = 0; i <= a; i++)
		for (int j = 0; j <= b; j++)
			for (int k = 0; k <= c; k++)
				for (int l = 0; l <= d; l++)
					if (!i || !j || !k || !l) dp[i][j][k][l] = 1ll;
					else {
						dp[i][j][k][l] = dp[i-1][j][k][l];
						ib = lb[j][A[i-1]-'a'], ic = lc[k][A[i-1]-'a'], id = ld[l][A[i-1]-'a'];
						if (ib && ic && id) {
							dp[i][j][k][l] += dp[i-1][ib-1][ic-1][id-1];
							ia = la[i-1][A[i-1]-'a'];
							if (ia) dp[i][j][k][l] -= dp[ia-1][ib-1][ic-1][id-1];
						}
					}
	printf("%lld\n", dp[a][b][c][d]-1ll);
}
