#include <stdio.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

const int BUFF_SIZE = 256;

int main()	{
	int n;
	scanf("%d", &n);
	char * a[n];
	int i, j;
	for(i = 0 ; i < n; i++)	{
		a[i] = malloc(BUFF_SIZE);
		scanf("%s", a[i]);
	}

	for(j = 1; j < n; j++)
		for(int k = j - 1; k >= 0; k--)	{
			if(strcmp(a[k], a[k + 1]) > 0)	{
				char * tmp = a[k + 1];
				a[k + 1] = a[k];
				a[k] = tmp;
			}
	}

	printf("Sorted:\n");
	for(i = 0; i < n; i++)
		printf("%s\t", a[i]);
	
	printf("\nUnique:\n%s\t", a[0]);
	for(i = 1; i < n; i++)
		if(strcmp(a[i], a[i-1]) != 0)
			printf("%s\t", a[i]);
	printf("\n");
	return 0;
}
