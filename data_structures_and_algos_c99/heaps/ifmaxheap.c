#include <stdio.h>

#define left(i) 2 * i + 1
#define right(i) left(i) + 1

int ifmaxheap(int *, int, int);

int main()
{
	int t;
	scanf("%d", &t);

	for (int i = 0; i < t; i++)
	{
		int n;
		scanf("%d", &n);
		int a[n];

		for (int j = 0; j < n; j++)
			scanf("%d", a + j);

		printf("%s\n", ifmaxheap(a, 0, n) ? "yes" : "no");
	}
}

int ifmaxheap(int *a, int i, int n)
{
	if (left(i) >= n)
		return 1;
	if ((a[i] < a[left(i)]) || ((right(i) < n) && (a[i] < a[right(i)])))
		return 0;
	return ifmaxheap(a, left(i), n) && ((right(i) < n) ? ifmaxheap(a, right(i), n) : 1);
}
