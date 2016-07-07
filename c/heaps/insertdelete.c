#include <stdio.h>
#include <stdlib.h>

#define left(i) 2 * i + 1
#define right(i) 2 * i + 2
#define parent(i) (i - 1) / 2

typedef struct heap	{
	int * a;
	int size;
	int capacity;
} maxheap;

void heapify(maxheap *, int);
void insert(int, maxheap *);
void display(maxheap *);
void delete(int, maxheap *);
int search(int, maxheap *, int);
void resize(maxheap *);
void reduce(maxheap *);

int main()
{
	int choice;
	maxheap h;
	h = (maxheap) {malloc(sizeof(int)), 0, 1};
	while (scanf("%d", &choice) > 0)	{
		int key;
		switch (choice)	{
			case 1:	scanf("%d", &key);
				insert(key, &h);	break;
			case 2: scanf("%d", &key);
				delete(key, &h);	break;
			case 3: display(&h);		break;
			case 4: return 0;
			default: return 1;
		}
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

void insert(int key, maxheap * h)
{
	if (h->size == h->capacity)
		resize(h);
	h->a[h->size] = key;
	for (int i = h->size; (parent(i) >= 0) && (key > h->a[parent(i)]); i = parent(i))	{
		int temp;
		temp = h->a[parent(i)];
		h->a[parent(i)] = key;
		h->a[i] = temp;
	}
	h->size++;
	printf("inserted\n");
}

void display(maxheap * h)
{
	for (int j = 0; j < h->size; j++)
		printf("%d ", h->a[j]);
	printf("\n");
}

void delete(int key, maxheap * h)
{
	if (!h->size)
		return;
	int i;
	if((i = search(key, h, 0)) == -1)	{
		printf("%d not found\n", key);
		return;
	}
	h->a[i] = h->a[h->size - 1];
	h->size--;
	heapify(h, 0);
	if ((h->size) && (h->size == h->capacity / 4))
		reduce(h);
	printf("deleted\n");
}

int search(int key, maxheap * h, int i)
{
	if (i > h->size - 1)
		return -1;
	if (h->a[i] == key)
		return i;
	if (key > h->a[i])
		return -1;
	if (key < h->a[i])	{
		int j;
		if ((j = search(key, h, left(i))) == -1)
			return search(key, h, right(i));
		else return j;
	}
}

void resize(maxheap * h)
{
	int * temp;
	h->capacity *= 2;
	temp = realloc(h->a, h->capacity * sizeof(int));
	if (!temp)
		exit(2);
	h->a = temp;
}

void reduce(maxheap *h)
{
	int * temp;
	h->capacity /= 2;
	temp = realloc(h->a, h->capacity * sizeof(int));
	if (!temp)
		exit(2);
	h->a = temp;
}
