#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void check(char *);

const int BUFF_SIZE = 256;

int main()	{
	int n, i;
	scanf("%d", &n);
	char * a[n];
	for(i = 0; i < n; i++)	{
		a[i] = malloc(BUFF_SIZE);
		scanf("%s", a[i]);
	}
	for(i = 0; i < n; i++)
		check(a[i]);
	return 0;
}

void check(char *s)	{
	int i, n = strlen(s), flag = 1;
	for(i = 0; i < n; i++)
		if(*(s + i) != *(s + (n - 1 - i)))	{
			flag = 0;
			break;
		}
	if(flag)
		printf("yes\n");
	else	printf("no\n");
}
