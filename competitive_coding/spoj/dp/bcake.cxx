#include <cstdio>
using namespace std;

int main()
{
	int t, h, w, k, n, res, a[31][31]{};
	char c;
	scanf("%d", &t);
	while (t--) {
		scanf("%d%d%d", &h, &w, &k);
		for (int i = 1; i <= h; i++)
			for (int j = 1; j <= w; j++) {
				scanf(" %c", &c);
				a[i][j] = a[i][j-1] + a[i-1][j] - a[i-1][j-1] + (c == 'C');
			}
		res = h * w + 1;
		for (int i = 1; i <= h; i++)
			for (int j = i; j <= h; j++)
				for (int l = 1; l <= w; l++)
					for (int m = l; m <= w; m++)
						if (a[j][m]-a[j][l-1]-a[i-1][m]+a[i-1][l-1] == k && (n = (j-i+1)*(m-l+1)) < res) res = n;
		printf("%d\n", res==h*w+1? -1 : res);
	}
}
