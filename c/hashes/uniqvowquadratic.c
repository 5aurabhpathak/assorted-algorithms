#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER 256
#define TABLE_SIZE 5
#define C1 1
#define C2 2

typedef struct hashtable_quadratic	{
	char * table;
	int size;
} hashtable_quadratic;

int hash_quadratic(char, hashtable_quadratic *);
void hashinsert(char, hashtable_quadratic *);
char * ht_to_array(hashtable_quadratic *, char *);
int compare(const void *, const void *);

void main()
{
	int n;
	scanf("%d", &n);

	char * word;
	hashtable_quadratic ht[n];
	for (int i = 0; i < n; i++)	{
		word = malloc(BUFFER);
		scanf("%s", word);
		ht[i] = (hashtable_quadratic) {calloc(TABLE_SIZE, 1), 0};
		for (int j = 0; j < strlen(word); j++)
			if((word[j] == 'a') || (word[j] == 'e') || (word[j] == 'i') || (word[j] == 'o') || (word[j] == 'u'))
				hashinsert(word[j], &ht[i]);

	}

	char * uniq[n];
	for (int i = 0; i < n; i++)	{
		uniq[i] = ht_to_array(&ht[i], uniq[i]);
		qsort(uniq[i], ht[i].size, 1, compare);
		for (int j = 0; j < ht[i].size; j++)
			printf("%c\t", *(uniq[i] + j));
		printf("\n");

	}

}

int hash_quadratic(char key, hashtable_quadratic * ht)
{
	return key % TABLE_SIZE;

}

void hashinsert(char key, hashtable_quadratic * ht)
{
	int pos;
	pos = hash_quadratic(key, ht);
	
	int i;
	i = 0;
	while (*(ht->table + pos) && (i < TABLE_SIZE))	{
		if (*(ht->table + pos) == key)
			return;
		pos = (pos + C1 * (++i) + C2 * (i ^ 2)) % TABLE_SIZE;

	}
	if (i < TABLE_SIZE)	{
		*(ht->table + pos) = key;
		ht->size++;

	}

}

char * ht_to_array(hashtable_quadratic * ht, char * uniq)
{
	int j;
	j = 0;
	uniq = malloc(ht->size);

	for (int i = 0; i < TABLE_SIZE; i++)
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
