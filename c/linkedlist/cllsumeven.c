#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <limits.h>

typedef struct node {
	int data;
	struct node * next;
} node;
const int BUFF = 256;

node * cllbuild();
node *  caddnode(node *, int);

int main()	{
	node * head = NULL;
	head = cllbuild();

	//sum of even numbers
	int sum = 0;
	node * cur = head;
	do	{
		if(cur->data % 2 == 0)
			sum += cur->data;
		cur = cur->next;
	} while(cur != head);

	//display
	printf("Sum: %d\n", sum);
	
	return 0;
}

node * caddnode(node * list, int value)	{
	node * new = malloc(sizeof(node));
	if(list == NULL)	{
		*new = (node){value, new};
		return new;
	}
	*new = (node){value, list};
	node * cur;
	for(cur = list; cur->next != list; cur = cur->next);
	cur->next = new;		
	return new;
}

node * cllbuild()	{
	char * list = malloc(BUFF);
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
