#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct node {
	int data;
	struct node * next;
} node;
const int BUFF = 256;

node * cllbuild();
node * caddnode(node *, int);
node * biggest(node *);
void cdisplay(node *);

int main()	{
	node * head = cllbuild();
	getchar();
	node *head2 = cllbuild();
	
	//merge clists by max
	node * inithead = head;
	head = biggest(head);
	head2 = biggest(head2);
	node * cur;
	for(cur = head2; cur->next != head2; cur = cur->next);
	node * tail = head->next;
	head->next = head2;
	cur->next = tail;

	//display
	cdisplay(inithead);
	
	return 0;
}

void cdisplay(node * list)	{
	node * cur = list;
	do	{
		printf("%d -> ", cur->data);
		cur = cur->next;
	} while(cur != list);
	printf("NULL\n");
}

node * biggest(node * list)	{
	int max = list->data;
	node * cur = list->next, * inithead = list;
	do	{
		if(cur->data > max)	{
			max = cur->data;
			list = cur;
		}
		cur = cur->next;
	} while(cur != inithead);
	return list;
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
	return list;
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
