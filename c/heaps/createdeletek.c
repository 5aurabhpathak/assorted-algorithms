#include <stdio.h>
#include <stdlib.h>

#define left(i) 2 * i + 1
#define right(i) 2 * i + 2
#define parent(i) (i - 1) / 2

typedef struct heap	{
	int * a;
	int size;
} minheap;

void heapify(minheap *, int);
void buildminheap(minheap *);
void display(minheap *);
void deleteroot(minheap *);

int main()
{
	int t;
	scanf("%d", &t);

	minheap h[t];
	int k[t];
	for (int i = 0; i < t; i++)	{
		int n;
		scanf("%d%d", &n, &k[i]);
		h[i] = (minheap) {malloc(n * sizeof(int)), n};
		for (int j = 0; j < n; j++)
			scanf("%d", h[i].a + j);
		buildminheap(&h[i]);
	}

	for (int i = 0; i < t; i++)	{
		display(&h[i]);
		for (int j = 0; j < k[i]; j++)
			deleteroot(&h[i]);
		display(&h[i]);
	}
}

void heapify(minheap * h, int i)
{
	int smallest;
	int small_i;
	smallest = h->a[i];
	
	if ((left(i) < h->size) && (smallest > h->a[left(i)]))	{
		small_i = left(i);
		smallest = h->a[small_i];
	}
	if ((right(i) < h->size) && (smallest > h->a[right(i)]))	{
		small_i = right(i);
		smallest = h->a[small_i];
	}

	if (smallest != h->a[i])	{
		int temp;
		temp = h->a[i];
		h->a[i] = smallest;
		h->a[small_i] = temp;
		heapify(h, small_i);
	}
}

void buildminheap(minheap * h)
{
	for (int i = parent(h->size - 1); i >= 0; i--)
		heapify(h, i);
}

void display(minheap * h)
{
	for (int j = 0; j < h->size; j++)
		printf("%d ", h->a[j]);
	printf("\n");
}

void deleteroot(minheap * h)
{
	if (!h->size)
		return;
	h->a[0] = h->a[h->size - 1];
	h->size--;
	heapify(h, 0);
}
