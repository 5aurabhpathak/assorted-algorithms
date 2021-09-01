#include <stdio.h>

int main()	{
	int n;
	scanf("%d", &n);
	int a[n][n];
	for(int i = 0; i < n; i++)
		for(int j = 0; j < n; j++)
			scanf("%d", &a[i][j]);
	int sum, maxindex, max = 0;
	for(int i = 0; i < n; i++)	{
		sum = 0;
		if((i >= 0) && (i<n-1))
			sum += a[i][i+1] + a[i+1][i] + a[i+1][i+1];
		if((i <= n-1) && (i>0))
			sum += a[i][i-1] + a[i-1][i] + a[i-1][i-1];
		if((i > 0) && ( i < n-1))
			sum += a[i+1][i-1] + a[i-1][i+1];
		printf("%d: %d\n", a[i][i], sum);
		if(sum > max)	{
			max = sum;
			maxindex = i + 1;
		}
	}
	printf("index: %d\n", maxindex);
	return 0;
}
