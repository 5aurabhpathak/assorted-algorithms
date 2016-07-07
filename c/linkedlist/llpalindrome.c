#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct node {
	char * data;
	struct node * next;
} node;
const int BUFF = 256;

node * llbuild();
node *  addnode(node *, char *);
node * traverse(node *, int);
int length(node *);
char * strrev(char *);

int main()	{
	node * head = NULL;
	head = llbuild();

	//palindrome or not!
	int i;
	node * cur;
	for(cur = head, i = 0; cur; cur = cur->next, i++)
		if(strcmp(cur->data, strrev((traverse(head, length(head) - i))->data)))	{
			printf("not palindrome\n");
			return 0;
		}
	printf("palindrome\n");

	return 0;
}

char * strrev(char * str)	{
	int length = strlen(str), i;
	char * rev = malloc(length);
	for(i = 0; i < length; i++)
		rev[i] = str[length -1 - i];
	rev[i] = '\0';
	return rev;
}

node * traverse(node * list, int index)	{
	node * cur = list;
	for(int i = 2; i <= index; i++)
		cur = cur->next;
	return cur;
}

int length(node * list)	{
	int count = 1;
	node * cur = list;
	if(cur == NULL)
		return 0;
	while(cur->next != NULL)	{
		cur = cur->next;
		count++;
	}
	return count;
}

node * addnode(node * list, char * value)	{
	node * end = traverse(list, length(list));
	node * new = malloc(sizeof(node));
	*new = (node){value, NULL};
	if(end == NULL)
		list = new;
	else
		end->next = new;
	return list;
}

node * llbuild()	{
	char * list = malloc(BUFF);
	scanf("%[^\n]", list);
	node * head = NULL;
	char * token = strtok(list, " -> ");
	while(strcmp(token, "NULL"))	{
		head = addnode(head, token);
		token = strtok(NULL, " -> ");
	}
	return head;
}
