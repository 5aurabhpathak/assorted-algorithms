#include <stdio.h>
#include <stdlib.h>

#define left(i) 2 * i + 1
#define right(i) 2 * i + 2
#define parent(i) (i - 1) / 2

typedef struct heap	{
	int * a;
	int size;
} maxheap;

int heapify(maxheap *, int);
int buildmaxheap(maxheap *);

int main()
{
	int t;
	scanf("%d", &t);

	maxheap h[t];
	int k[t];
	for (int i = 0; i < t; i++)	{
		int n;
		scanf("%d", &n);
		h[i] = (maxheap) {malloc(n * sizeof(int)), n};
		for (int j = 0; j < n; j++)
			scanf("%d", h[i].a + j);
		k[i] = buildmaxheap(&h[i]);
	}

	for (int i = 0; i < t; i++)
		printf("%d\n", k[i]);
}

int heapify(maxheap * h, int i)
{
	int largest;
	int large_i;
	largest = h->a[i];
	
	if ((left(i) < h->size) && (largest < h->a[left(i)]))	{
		large_i = left(i);
		largest = h->a[large_i];
	}
	if ((right(i) < h->size) && (largest < h->a[right(i)]))	{
		large_i = right(i);
		largest = h->a[large_i];
	}

	if (largest != h->a[i])	{
		int temp;
		temp = h->a[i];
		h->a[i] = largest;
		h->a[large_i] = temp;
		return 1 + heapify(h, large_i);
	}
	return 0;
}

int buildmaxheap(maxheap * h)
{
	int numswaps;
	numswaps = 0;
	for (int i = parent(h->size - 1); i >= 0; i--)
		numswaps += heapify(h, i);
	return numswaps;
}
