#include <stdio.h>
#include <limits.h>

int main()	{
	printf("Enter dimension n(nxn):");
	int n, sum = 0;
	scanf("%d", &n);
	int d[n];
	printf("Enter diagonal elements:");
	for(int i = 0; i < n; i++)	{
		scanf("%d", &d[i]);
		sum += d[i];
	}
	int others;
	if(sum >= 0)
		others = sum / (n * n - n) + 1;
	else others = INT_MIN;
	for(int i = 0; i < n; i++)	{
		for(int j = 0; j < n; j++)
			if(i == j)
				printf("%d\t", d[i]);
			else
				printf("%d\t", others);
		printf("\n");
	}
}
