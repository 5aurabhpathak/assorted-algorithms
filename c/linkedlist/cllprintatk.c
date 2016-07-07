#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct node {
	int data;
	struct node * next;
} node;
const int BUFF = 256;

node * cllbuild();
node *  caddnode(node *, int);
node * ctraverse(node *, int);
int clength(node *);

int main()	{
	node * head = NULL;
	int k;
	scanf("%d", &k);
	head = cllbuild();

	//index skip k - 1 traversal
	node * cur = head;
	int len = clength(head), count = 0;
	do	{
		printf("%d -> ", cur->data);
		count++;
		if(count == len)
			break;
		for(int i = k; i > 0; i--)
			cur = cur->next;
	} while(1);

	printf("NULL\n");
	return 0;
}

node * ctraverse(node * list, int index)	{
	node * cur = list;
	for(int i = 2; i <= index; i++)
		cur = cur->next;
	return cur;
}

int clength(node * list)	{
	int count = 1;
	node * cur = list;
	if(cur == NULL)
		return 0;
	while(cur->next != list)	{
		cur = cur->next;
		count++;
	}
	return count;
}

node * caddnode(node * list, int value)	{
	node * end = ctraverse(list, clength(list));
	node * new = malloc(sizeof(node));
	*new = (node){value, list};
	if(end == NULL)	{
		list = new;
		list->next = list;
	}
	else
		end->next = new;
	return list;
}

node * cllbuild()	{
	char * list = malloc(BUFF);
	getchar();
	scanf("%[^\n]", list);
	node * head = NULL;
	char * token = strtok(list, " ");
	while(token != NULL)	{
		char * endptr = NULL;
		int val = strtol(token, &endptr, 10);
		if(!*endptr)
			head = caddnode(head, val);
		token = strtok(NULL, " ");
	}
	return head;
}
