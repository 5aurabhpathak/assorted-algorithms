#include <stdio.h>
#define max(a, b) a > b ? a : b
int knapsack(int, int, int, int [], int [], int (*)[]);

int main()
{
	int w, n;
	scanf("%d%d", &w, &n);
	int wt[n], v[n], mem[n+1][w+1];
	for (int i = 0; i < n; i++) 	{
		scanf("%d%d", &wt[i], &v[i]);
		for (int j = 0; j < w+1; j++)
			mem[i][j] = 0;
	}
	for (int i = 0; i < w+1; i++)
		mem[n][i] = 0;
	printf("%d\n", knapsack(w, n, w, wt, v, mem));
}

int knapsack(int W, int n, int w, int wt[], int v[], int (*mem)[W])
{
	if ((n == 0) || (w == 0))
		return 0;
	if (mem[n][w] != 0)
		return mem[n][w];
	if (wt[n - 1] > w)
		mem[n][w] = knapsack(W, n - 1, w, wt, v, mem);
	else
		mem[n][w] = max(knapsack(W, n - 1, w, wt, v, mem), v[n - 1] + knapsack(W, n - 1, w - wt[n - 1], wt, v, mem));
	return mem[n][w];
}
