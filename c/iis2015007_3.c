#include <stdio.h>
#include <stdlib.h>

typedef struct cnode {
	int data;
	struct cnode * next;
} cnode;

int length(cnode *);
cnode * traverse(cnode *, int);
cnode * caddnode(cnode *, int);
void display(cnode *);
cnode * llcopy(cnode *);

int main()
{

	int n;
	int t;
	
	scanf("%d", &t);

	cnode * lists[t]; 

	for (int i = 0; i < t; i++)	{
		cnode * cur;
		cnode * copy;
		cnode * tmp;
		cnode * copyend;

		lists[i] = NULL;

		scanf("%d", &n);
		for (int j = 0; j < n; j++)	{
			int val;
			scanf("%d", &val);
			lists[i] = caddnode(lists[i], val);

		}

		cur = traverse(lists[i], length(lists[i])/2);
		copy = llcopy(lists[i]);
		tmp = cur->next;
		cur->next = copy;
		copyend = traverse(copy, length(copy));
		copyend->next = tmp;
		tmp = traverse(lists[i], length(lists[i]));
		lists[i] = tmp;

	}

	for(int i = 0; i < t; i++)
		display(lists[i]);

	return 0;

}

cnode * llcopy(cnode * head)
{
	cnode * new;
	cnode * cur;

	new = NULL;

	for (cur = head; cur->next != head; cur = cur->next)
		new = caddnode(new, cur->data);
	new = caddnode(new, cur->data);
	
	return new;
	
}

int length(cnode * head)
{
	int l;
	cnode * cur;

	l = 1;
	cur = head;
	if(!cur)
		return 0;

	while (cur->next != head)	{
		l++;
		cur = cur->next;
	}
	return l;

}

cnode * traverse(cnode * head, int index)
{
	cnode * cur;
	int i;

	cur = head;
	
	if (!((index > 0) && (index <= length(head))))
		return NULL;
	for (i = 2; i <= index; i++)
		cur = cur->next;
	return cur;

}

cnode * caddnode(cnode * head, int val)
{
	cnode * end;
	cnode * new;

	end = traverse(head, length(head));
	new = malloc(sizeof(cnode));

	if (!end)	{
		*new = (cnode){val, new};
		return new;
	}
	else	{
		*new = (cnode){val, head};
		end->next = new;
	}
	return head;

}

void display(cnode * head)
{
	cnode * cur;

	cur = head;

	while (cur->next != head)	{
		printf("%d ", cur->data);
		cur = cur->next;
	}
	printf("%d\n", cur->data);

}
