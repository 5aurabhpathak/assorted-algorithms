#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct node {
	int data;
	struct node * next;
} node;
const int BUFF = 256;

node * llbuild();
node *  addnode(node *, int);
node * traverse(node *, int);
int length(node *);
node * grpreverse(node *, int);
void display(node *);

int main()	{
	node * head = NULL;
	int k;
	scanf("%d", &k);
	head = llbuild();
//	display(head);

	//group reversal by k indices: divide and conquer approach
	head = grpreverse(head, k);

	//display
	display(head);
	
	return 0;
}

node * grpreverse(node * list, int k)	{
	node *cur = list, * prev = NULL;
	int i = 0;
	while((i < k) && (cur != NULL))	{
		node * next = cur->next;
		cur->next = prev;
		prev = cur;
		cur = next;
		i++;
	}
	if(cur)
		list->next = grpreverse(cur, k);
	list = prev;
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
	getchar();
	scanf("%[^\n]", list);
	node * head = NULL;
	char * token = strtok(list, " ");
	while(token != NULL)	{
		char * endptr = NULL;
		int val = strtol(token, &endptr, 10);
		if(!*endptr)
			head = addnode(head, val);
		token = strtok(NULL, " ");
	}
	return head;
}
