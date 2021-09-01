#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

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

	//smallest
	int smallest = INT_MAX;
	for(node * cur = head; cur != NULL; cur = cur->next)
		if(cur->data < smallest)
			smallest = cur->data;
	
	//delete
	for(node * cur = head; cur != NULL; cur = cur->next)
		if(cur->data == smallest)	{
			if(cur == head)	{	//first element
				head = cur->next;
				head->prev = NULL;
			}
			else if(cur->next == NULL)	//last element
				cur->prev->next = NULL;
			else	{	//other cases
				cur->prev->next = cur->next;
				cur->next->prev = cur->prev;
			}
		}

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
