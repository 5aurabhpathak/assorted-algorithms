#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER 256
#define TABLE_SIZE 5

typedef struct node	{
	char data;
	struct node * next;
} node;

typedef struct hashtable_chain	{
	node ** table;
	int size;
} hashtable_chain;

int hash_chain(char);
void hashinsert(char, hashtable_chain *);
char * ht_to_array(hashtable_chain *, char *);
int chain_contains_key(node *, char);
node * addnode(node *, char);
int compare(const void *, const void *);

void main()
{
	int n;
	scanf("%d", &n);

	char * words[n];
	hashtable_chain ht[n];
	for (int i = 0; i < n; i++)	{
		words[i] = malloc(BUFFER);
		scanf("%s", words[i]);
		ht[i] = (hashtable_chain) {calloc(TABLE_SIZE, sizeof(node *)), 0};

	}
	for (int i = 0; i < n; i++)
		for (int j = 0; j < strlen(words[i]); j++)
			hashinsert(words[i][j], &ht[i]);

	char * uniq[n];
	for (int i = 0; i < n; i++)	{
		uniq[i] = ht_to_array(&ht[i], uniq[i]);
		qsort(uniq[i], ht[i].size, 1, compare);
		for(int j = 0; j < ht[i].size; j++)
			printf("%c\t", *(uniq[i] + j));
		printf("\n");

	}

}

int hash_chain(char key)
{
	return key % TABLE_SIZE;

}

void hashinsert(char key, hashtable_chain * ht)
{
	int pos;
	pos = hash_chain(key);
	if (!chain_contains_key(*(ht->table + pos), key))	{
		*(ht->table + pos) = addnode(*(ht->table + pos), key);
		ht->size++;

	}

}

int chain_contains_key(node * head, char key)
{
	if (!head)
		return 0;
	for (node * cur = head; cur; cur = cur->next)
		if (cur->data == key)
			return 1;
	return 0;

}


node * addnode (node * head, char data)
{
	node * new;
	new = malloc(sizeof(node));
	*new = (node) {data, head};
	return new;

}

char * ht_to_array(hashtable_chain * ht, char * uniq)
{
	int j;
	j = 0;
	uniq = malloc(ht->size);

	for (int i = 0; i < TABLE_SIZE; i++)
		if (*(ht->table + i))
			for (node * cur = *(ht->table + i); cur; cur = cur->next, j++)
				*(uniq + j) = cur->data;
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
