//implementation of linear probe hash with dynamic table and rehashing support
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER 256
#define INITIAL_SIZE 5

typedef struct hashtable_linear	{
	char * table;
	int size;
	int capacity;
} hashtable_linear;

int hash_linear(char, hashtable_linear *);
void hashinsert(char, hashtable_linear *);
char * ht_to_array(hashtable_linear *, char *);
int compare(const void *, const void *);

void main()
{
	int n;
	scanf("%d", &n);

	char * words[n];
	hashtable_linear ht[n];
	for (int i = 0; i < n; i++)	{
		words[i] = malloc(BUFFER);
		scanf("%s", words[i]);
		ht[i] = (hashtable_linear) {calloc(INITIAL_SIZE, 1), 0, INITIAL_SIZE};

	}
	for (int i = 0; i < n; i++)
		for (int j = 0; j < strlen(words[i]); j++)
			hashinsert(words[i][j], &ht[i]);

	char * uniq[n];
	for (int i = 0; i < n; i++)	{
		uniq[i] = ht_to_array(&ht[i], uniq[i]);
		qsort(uniq[i], ht[i].size, 1, compare);
		for (int j = 0; j < ht[i].size; j++)
			printf("%c\t", *(uniq[i] + j));
		printf("\n");

	}

}

int hash_linear(char key, hashtable_linear * ht)
{
	return key % ht->capacity;

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
		pos = ++pos % ht->capacity;

	}
	if (i < ht->capacity)	{
		*(ht->table + pos) = key;
		ht->size++;

	}
	else	{
		char * arr;
		arr = ht_to_array(ht, arr);
		ht->capacity *= 2;
		char * tmp;
		tmp = NULL;
		while (!(tmp = realloc(ht->table, ht->capacity)));
		ht->table = tmp;
		
		ht->table = memset(ht->table, 0, ht->capacity);
		int oldsize;
		oldsize = ht->size;
		ht->size = 0;
		for (int i = 0; i < oldsize; i++)
			hashinsert(*(arr + i), ht);
		hashinsert(key, ht);

	}

}

char * ht_to_array(hashtable_linear * ht, char * uniq)
{
	int j;
	j = 0;
	uniq = malloc(ht->size);

	for (int i = 0; i < ht->capacity; i++)
		if (*(ht->table + i))
			*(uniq + j++) = *(ht->table + i);
	return uniq;

}

int compare(const void * a, const void * b)
{
	int aa;
	aa = *(char *)a;
	int bb;
	bb = *(char *)b;

	if (aa == bb)
		return 0;
	if(aa < bb)
		return -1;
	else return 1;

}
