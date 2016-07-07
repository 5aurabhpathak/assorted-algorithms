#include <stdio.h>
#include <stdlib.h>
 
struct tuple 	{
	long long x,y;
};

char compare(struct tuple a, struct tuple b)
{
	if ((a.x < b.x) && (a.y < b.y)) 	return -1;
	if ((a.x > b.x) && (a.y > b.y)) 	return 1;
	return 0;
}
 
unsigned long CeilIndex(struct tuple A[], unsigned long l, unsigned long r, struct tuple key)
{
     while (r - l > 1) {
	     unsigned long m = l + (r - l)/2;
	     if (compare(A[m], key) >= 0 )
		     r = m;
	     else
		     l = m;
     }
     return r;
}
                                                                
unsigned long LongestIncreasingSubsequenceLength(struct tuple A[], unsigned long size)
{
	struct tuple *tailTable = malloc(size * sizeof(struct tuple));
	int len = 1;
	tailTable[0] = A[0];
	for (unsigned long i = 1; i < size; i++)
		tailTable[i] = (struct tuple) {-10^10, -10^10};
	for (unsigned long i = 1; i < size; i++)
		if (compare(A[i], tailTable[0]) < 0)
			tailTable[0] = A[i];
	        else if (compare(A[i], tailTable[len - 1]) > 0)
			tailTable[len++] = A[i];
		else
			tailTable[CeilIndex(tailTable, -1, len-1, A[i])] = A[i];
	free(tailTable);
	return len;
}

int main()
{
	unsigned long n;
	scanf("%lu", &n);
	struct tuple A[n];
	for (unsigned long i = 0; i < n; i++)
		scanf("%lld%lld", &(A[i].x), &(A[i].y));
	printf("%lu\n", LongestIncreasingSubsequenceLength(A, n));
}
