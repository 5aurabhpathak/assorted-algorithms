#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

typedef struct node {
	struct node * prev;
	int data;
	struct node * next;
} node;

node * addnode(node *, int);

int main()	{
	int n;
	scanf("%d", &n);
	node * head = NULL;
	for(int i = 0; i < n; i++)	{
		int value;
		scanf("%d", &value);
		head = addnode(head, value);
	}

	//smallest
	int smallest = INT_MAX;
	for(node * cur = head; cur != NULL; cur = cur->next)
		if(cur->data < smallest)
			smallest = cur->data;

	//display
	printf("Smallest: %d\n", smallest);

	return 0;
}

node * addnode(node * list, int value)	{
	node * new = malloc(sizeof(node));
	*new = (node){NULL, value, list};
	if(list != NULL)
		list->prev = new;
	return new;
}
