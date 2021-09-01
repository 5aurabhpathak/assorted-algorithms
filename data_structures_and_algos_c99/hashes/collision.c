#include <stdio.h>
#include <stdlib.h>

#define BUFFER 256

typedef struct hashtable_linear	{
	int * table;
	int size;
	int capacity;
} hashtable_linear;

int hash_linear(char, hashtable_linear *);
void hashinsert(char, hashtable_linear *);

int numcollisions;

int main()
{
	int t;
	int k;
	int n;
	scanf("%d%d%d", &t, &k, &n);

	int data[t][k];
	hashtable_linear ht[t];
	for (int i = 0; i < t; i++)	{
		for(int j = 0; j < k; j++)
			scanf("%d", &data[i][j]);
		ht[i] = (hashtable_linear) {calloc(n, sizeof(int)), 0, n};

	}
	for (int i = 0; i < t; i++)	{
		numcollisions = 0;
		for (int j = 0; j < k; j++)
			hashinsert(data[i][j], &ht[i]);
	
	}

}

int hash_linear(char key, hashtable_linear * ht)
{
	return (key + 5) % ht->capacity;

}

void hashinsert(char key, hashtable_linear * ht)
{
	int pos;
	pos = hash_linear(key, ht);
	
	int i;
	i = 0;
	while (*(ht->table + pos) && (i++ < ht->capacity))	{
		if (*(ht->table + pos) == key)
			return;
		if(!numcollisions)
			printf("%d\n", key);
		numcollisions++;
		pos = ++pos % ht->capacity;

	}
	if (i < ht->capacity)	{
		*(ht->table + pos) = key;
		ht->size++;

	}

}
