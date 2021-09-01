#include <stdio.h>
#include <stdlib.h>

#define left(i) 2 * i + 1
#define right(i) 2 * i + 2
#define parent(i) (i - 1) / 2

typedef struct heap	{
	int * a;
	int size;
} maxheap;

void heapify(maxheap *, int);
void buildmaxheap(maxheap *);
void displayarray(maxheap *, int);
void extractmax(maxheap *);

int main()
{
	int t;
	scanf("%d", &t);

	maxheap h[t];
	int k[t];
	for (int i = 0; i < t; i++)	{
		int n;
		scanf("%d", &n);
		k[i] = n;
		h[i] = (maxheap) {malloc(n * sizeof(int)), n};
		for (int j = 0; j < n; j++)
			scanf("%d", h[i].a + j);
		buildmaxheap(&h[i]);
	}

	for (int i = 0; i < t; i++)	{
		for (int j = 0; j < k[i] - 1; j++)
			extractmax(&h[i]);
		displayarray(&h[i], k[i]);
	}
}

void heapify(maxheap * h, int i)
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
		heapify(h, large_i);
	}
}

void buildmaxheap(maxheap * h)
{
	for (int i = parent(h->size - 1); i >= 0; i--)
		heapify(h, i);
}

void displayarray(maxheap * h, int n)
{
	for (int j = 0; j < n; j++)
		printf("%d ", h->a[j]);
	printf("\n");
}

void extractmax(maxheap * h)
{
	if (!h->size)
		return;
	int temp = h->a[0];
	h->a[0] = h->a[h->size - 1];
	h->a[h->size -1] = temp;
	h->size--;
	heapify(h, 0);
}
