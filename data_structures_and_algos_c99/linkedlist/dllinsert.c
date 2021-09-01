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

	return 0;
}

void display(node * list)	{
	while(list != NULL)	{
		printf("%d -> ", list->data);
		list = list->next;
	}
	printf("NULL\n");
}

node * addnode(node * list, int value)	{
	node * new = malloc(sizeof(node));
	*new = (node){NULL, value, list};
	if(list != NULL)
		list->prev = new;
	return new;
}
