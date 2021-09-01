#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER 256
#define TABLE_SIZE 26

typedef	int * hashtable_direct;

int hash_direct(char);
void hashinsert(char, hashtable_direct);

void main()
{
	int n;
	scanf("%d", &n);

	char * word;
	hashtable_direct ht[n];
	for (int i = 0; i < n; i++)	{
		word = malloc(BUFFER);
		scanf("%s", word);
		ht[i] = calloc(TABLE_SIZE, sizeof(int));
		for (int j = 0; j < strlen(word); j++)
			hashinsert(word[j], ht[i]);

	}

	for(int j = 0; j < n; j++)	{
		for (int i = 0; i < TABLE_SIZE; i++)
			if(*(ht[j] + i))
				printf("%c\t%d\t", i + 'a', *(ht[j] +i));
		printf("\n");
	}

}

int hash_direct(char key)
{
	return key - 'a';

}

void hashinsert(char key, hashtable_direct ht)
{
	int pos;
	pos = hash_direct(key);
	(*(ht + pos))++;

}
