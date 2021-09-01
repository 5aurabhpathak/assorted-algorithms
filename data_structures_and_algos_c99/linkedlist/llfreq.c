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
int search(node *, int);

int main()	{
	node * head = llbuild();

	//frequency count orderwise
	node * uniq = NULL;
	for(node * cur  = head; cur; cur = cur->next)
		if(!search(uniq, cur->data))	{
			uniq = addnode(uniq, cur->data);
			int count = 1;
			for(node * cur2 = cur->next; cur2; cur2 = cur2->next)
				if(cur2->data == cur->data)
					count++;
			printf("Freq(%d) = %d\n", cur->data, count);
		}

	return 0;
}

int search(node * list, int key)	{
	int i;
	node * cur;
	for(cur = list, i = 1; cur; cur = cur->next, i++)
		if(cur->data == key)
			return i;
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
