#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER 256
#define TABLE_SIZE 26

typedef	char * hashtable_direct;

int hash_direct(char);
void hashinsert(char, hashtable_direct);

void main()
{
	int n;
	scanf("%d", &n);

	char * words[n];
	hashtable_direct ht[n];
	for (int i = 0; i < n; i++)	{
		words[i] = malloc(BUFFER);
		scanf("%s", words[i]);
		ht[i] = calloc(TABLE_SIZE, 1);

	}
	for (int i = 0; i < n; i++)
		for (int j = 0; j < strlen(words[i]); j++)
			if((words[i][j] == 'a') || (words[i][j] == 'e') || (words[i][j] == 'i') || (words[i][j] == 'o') || (words[i][j] == 'u'))
				hashinsert(words[i][j], ht[i]);

	for(int j = 0; j < n; j++)	{
		for (int i = 0; i < TABLE_SIZE; i++)
			if(*(ht[j] + i))
				printf("%c\t", *(ht[j] + i));
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
	if(!*(ht + pos))
		*(ht + pos) = key;

}
