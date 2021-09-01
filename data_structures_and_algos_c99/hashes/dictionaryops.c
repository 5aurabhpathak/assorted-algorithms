#include <stdio.h>
#include <stdlib.h>

#define BUFFER 256

typedef struct hashtable_linear	{
	int * table;
	int size;
	int capacity;
} hashtable_linear;

int hash_linear(int, hashtable_linear *);
void hashinsert(int, hashtable_linear *);
void hashdelete(int, hashtable_linear *);
int hashsearch(int, hashtable_linear *);

void main()
{
	int n;
	scanf("%d", &n);
	hashtable_linear ht;
	ht = (hashtable_linear)	{calloc(n, sizeof(int)), 0, n};

	while (scanf("%d", &n) > 0)	{
		int data;
		if (!n)
			exit (0);
		scanf("%d", &data);
		switch (n)	{
			case 1: hashinsert(data, &ht);	break;
			case 2: hashdelete(data, &ht);	break;
			case 3: if (hashsearch(data, &ht) != -1)
					printf("Found\n");
				else
					printf("Not found\n");

		}

	}

}

int hash_linear(int key, hashtable_linear * ht)
{
	return key % ht->capacity;

}

void hashinsert(int key, hashtable_linear * ht)
{
	int pos;
	pos = hash_linear(key, ht);
	
	int i;
	i = 0;
	while (*(ht->table + pos) && (i < ht->capacity))	{
		if (*(ht->table + pos) == key)	{
			printf("Not inserted\n");
			return;

		}
		else if (*(ht->table + pos) == -1)
			break;
		pos = ++pos % ht->capacity;
		i++;

	}
	if (i < ht->capacity)	{
		*(ht->table + pos) = key;
		ht->size++;
		printf("Inserted\n");

	}
	else	{
		printf("Not inserted\n");
		exit(1);
	}

}

void hashdelete(int key, hashtable_linear * ht)
{
	int pos;

	if ((pos = hashsearch(key, ht)) != -1)	{
		*(ht->table + pos) = -1;
		ht->size--;
		printf("Deleted\n");

	}
	else
		printf("Not deleted\n");

}

int hashsearch(int key, hashtable_linear * ht)
{
	int pos;
	pos = hash_linear(key, ht);

	int i;
	i = 0;

	while (*(ht->table + pos) && ( i < ht->capacity))	{
		if (*(ht->table + pos) == key)
			return pos;
		pos = ++pos % ht->capacity;
		i++;

	}

	return -1;

}
