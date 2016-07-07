#include <stdio.h>

void main()	{
	int i, j, a[5][5], sum[5];
	for(i = 0; i < 5; i++)
		scanf("%d %d %d %d %d", &a[i][0], &a[i][1],
					&a[i][2], &a[i][3],
					&a[i][4]);
	for(i = 0; i < 5; i++)	{
		if( i == 0)
			sum[i] = a[i][i+1] + a[i+1][i+1] + a[i+1][i];
		else if(i == 4)
			sum[i] = a[i][i-1] + a[i-1][i-1] + a[i-1][i];
		else
			sum[i] = a[i][i+1] + a[i+1][i+1] + a[i+1][i]
				+a[i][i-1] + a[i-1][i-1] + a[i-1][i]
				+a[i-1][i+1] + a[i+1][i-1];
		printf("%d: %d\n", a[i][i], sum[i]);
	}
	
	int max=0, index;
	for(i = 0; i < 5 ; i++)
		if(sum[i] > max)	{
			max = sum[i];
			index = i+1;
	}
	printf("index: %d\n", index);
}
