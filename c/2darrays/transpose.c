#include <stdio.h>
#include <stdlib.h>

int ** transpose(int *pm, int *pn, int (*arr)[*pn])	{

	int *c;
	int **t = (int **) malloc(*pn*sizeof(int *));
	int i, j;
	for(i = 0; i < *pn; i++)	{
		c = (int *) malloc(*pm*sizeof(int));
		*(t+i) = c;
		for(j = 0; j < *pm; j++)
			*(c+j) = arr[j][i];
	}
	return t;
}

int main()	{
	int m, n;
	scanf("%d%d", &m, &n);
	int arr[m][n];
	for(int i = 0; i < m; i++)
		for(int j = 0; j < n; j++)
			scanf("%d", &arr[i][j]);
	int **result;
	result = transpose(&m, &n, arr);
	for(int i = 0; i < n; i++)	{
		for(int j = 0; j < m; j++)
			printf("%d\t", result[i][j]);
		printf("\n");
	}
	free(result);
	return 0;
}
