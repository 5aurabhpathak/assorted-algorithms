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
node * copy(node *);
node * traverse(node *, int);
int length(node *);
void display(node *);

int main()	{
	int value, k;
	scanf("%d%d", &value, &k);
	node * head = NULL;
	head = llbuild();
//	display(head);

	//at the beginning
	node * head1 = copy(head);
	node * new = malloc(sizeof(node));
	*new = (node){value, head1};
	head1 = new;

	//at the end
	node * head2 = copy(head);
	head2 = addnode(head2, value);

	//at a given position k
	node * head3 = copy(head);
	new = malloc(sizeof(node));
	if(k == 1)	{
		*new = (node){value, head3};
		head3 = new;
	}
	else	{
		node * end = traverse(head3, k - 1);
		*new = (node){value, end->next};
		end->next = new;
	}

	//display
	display(head1);
	display(head2);
	display(head3);
	
	return 0;
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

node * copy(node * list)
{
	int i = 0, len = length(list);
	int data[len];
	node * newhead = NULL;
	node * cur = list;
	while(cur != NULL)	{
		data[i++] = cur->data;
		cur = cur->next;
	}
	for(i = 0; i < len; i++)
		newhead = addnode(newhead, data[i]);
	return newhead;
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
