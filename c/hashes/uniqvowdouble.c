#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER 256
#define TABLE_SIZE 5

typedef struct hashtable_double	{
	char * table;
	int size;
} hashtable_double;

int hash_double1(char, hashtable_double *);
int hash_double2(char, hashtable_double *);
void hashinsert(char, hashtable_double *);
char * ht_to_array(hashtable_double *, char *);
int compare(const void *, const void *);

void main()
{
	int n;
	scanf("%d", &n);

	char * word;
	hashtable_double ht[n];
	for (int i = 0; i < n; i++)	{
		word = malloc(BUFFER);
		scanf("%s", word);
		ht[i] = (hashtable_double) {calloc(TABLE_SIZE, 1), 0};
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

int hash_double1(char key, hashtable_double * ht)
{
	return key % TABLE_SIZE;

}

int hash_double2(char key, hashtable_double * ht)
{
	return 1 + key % (TABLE_SIZE - 1);

}

void hashinsert(char key, hashtable_double * ht)
{
	int pos;
	pos = hash_double1(key, ht);
	
	int i;
	i = 0;
	while (*(ht->table + pos) && (i < TABLE_SIZE))	{
		if (*(ht->table + pos) == key)
			return;
		pos = (pos + (++i) * hash_double2(key, ht)) % TABLE_SIZE;

	}
	if (i < TABLE_SIZE)	{
		*(ht->table + pos) = key;
		ht->size++;

	}

}

char * ht_to_array(hashtable_double * ht, char * uniq)
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
