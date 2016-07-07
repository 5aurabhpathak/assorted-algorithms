#include <stdio.h>
#include <stdlib.h>

typedef struct node {
	struct node * prev;
	int data;
	struct node * next;
} node;

node * addnode(node *, int);
void display(node *);

int main()	{
	int n;
	scanf("%d", &n);
	node * head = NULL;
	for(int i = 0; i < n; i++)	{
		int value;
		scanf("%d", &value);
		head = addnode(head, value);
	}
	display(head);

	//reversal
	node * cur = head, *previous;
	while(cur != NULL)	{
		previous = cur->prev;
		cur->prev = cur->next;
		node * next = cur->next;
		cur->next = previous;
		cur = next;
	}
	if(previous != NULL)
		head = previous->prev;

	//display
	display(head);
	return 0;
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

node * addnode(node * list, int value)	{
	node * new = malloc(sizeof(node));
	if(list == NULL)	{
		*new = (node){NULL, value, NULL};
		list = new;
	}
	else	{
		node * end = traverse(list, length(list));
		*new = (node){end, value, NULL};
		end->next = new;
	}
	return list;
}

void display(node * list)	{
	node * new = list;
	while(new != NULL)	{
		printf("%d -> ", new->data);
		new = new->next;
	}
	printf("NULL\n");
}
