//implementation of linear hash with dynamic table and rehashing support
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER 256
#define INITIAL_SIZE 5

typedef struct hashtable_linear	{
	char ** table;
	int size;
	int capacity;
} hashtable_linear;

int hash_linear(char *, hashtable_linear *);
void hashinsert(char *, hashtable_linear *);
char ** ht_to_array(hashtable_linear *, char **);

void main()
{
	int n;
	scanf("%d", &n);

	char * word;
	hashtable_linear ht;
	ht = (hashtable_linear) {calloc(INITIAL_SIZE, sizeof(char *)), 0, INITIAL_SIZE};
	for (int i = 0; i < n; i++)	{
		word = malloc(BUFFER);
		scanf("%s", word);
		hashinsert(word, &ht);

	}

	printf("%d\n", ht.size);

}

int hash_linear(char * key, hashtable_linear * ht)
{
	//djb2 algorithm. Copied! I don't understand this hash function or how it works
	unsigned long h;
	h = 5381;
	int c;
	while (c = *key++)
		h = ((h << 5) + h) + c;
	return h % ht->capacity;

}

void hashinsert(char * key, hashtable_linear * ht)
{
	int pos;
	pos = hash_linear(key, ht);
	
	int i;
	i = 0;
	while (*(ht->table + pos) && (i < ht->capacity))	{
		if (!strcmp(*(ht->table + pos), key))
			return;
		pos = (pos + (++i)) % ht->capacity;

	}
	if (i < ht->capacity)	{
		*(ht->table + pos) = key;
		ht->size++;

	}
	else	{
		char ** arr;
		arr = ht_to_array(ht, arr);
		ht->capacity *= 2;
		char ** tmp;
		while (!(tmp = realloc(ht->table, ht->capacity * sizeof(char *))));
		ht->table = tmp;
		
		ht->table = memset(ht->table, 0, ht->capacity * sizeof(char *));
		int oldsize;
		oldsize = ht->size;
		ht->size = 0;
		for (int i = 0; i < oldsize; i++)
			hashinsert(*(arr + i), ht);
		hashinsert(key, ht);

	}

}

char ** ht_to_array(hashtable_linear * ht, char ** uniq)
{
	int j;
	j = 0;
	uniq = malloc(ht->size * sizeof(char *));

	for (int i = 0; i < ht->capacity; i++)
		if (*(ht->table + i))
			*(uniq + j++) = *(ht->table + i);
	return uniq;

}
