#include <stdio.h>

int main()	{
	int n;
	scanf("%d", &n);
	int a[n][n];
	int rowsum[n], columnsum[n], sum1, sum2, i, j;
	for(i = 0; i < n; i++)
		for(j = 0; j < n; j++)
			scanf("%d", &a[i][j]);

	for(i = 0; i < n; i++)	{
		sum1 = sum2 = 0;
		for(j = 0; j < 4; j++)	{
			sum1 += a[i][j];
			sum2 += a[j][i];
		}
		rowsum[i] = sum1;
		columnsum [i] = sum2;
	}
	
	for(i = 0; i < n; i++)
		for(j = 0; j < n; j++)
			if(rowsum[i] == columnsum[j])
				printf("Row: %d\nColumn: %d\n", i+1, j+1);
	return 0;
}
