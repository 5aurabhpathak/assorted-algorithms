#include <stdio.h>

int main()	{
	int n;
	scanf("%d", &n);
	int a[n][n];
	for(int i = 0; i < n; i++)
		for(int j = 0; j < n; j++)
			scanf("%d", &a[i][j]);
	int sum, flag = 1;
	for(int i = 0; i < n; i++)	{
		sum = 0;
		if((i >= 0) && (i<n-1))
			sum += a[i][i+1] + a[i+1][i];
		if((i <= n-1) && (i>0))
			sum += a[i][i-1] + a[i-1][i];
		if(sum != a[i][i])	{
			flag = 0;
			break;
		}
	
	}
	if(flag)
		printf("yes");
	else	printf("no");
	return 0;
}
