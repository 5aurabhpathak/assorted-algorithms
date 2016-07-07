#include <stdio.h>
#include <stdlib.h>

typedef struct node {
	int data;
	struct node * next;
	struct node * friend;
} node;

typedef struct entry	{
	node * original;
	node * copy;
} entry;

typedef struct table	{
	entry *tbl;
	int n;
	int (*h)(node *, struct table *);
} table;

node * addnode(node *, int);
void addfriends(node *, int[], int);
int hasher(node *, table *);
node * get(table, node *);

void main()
{
	int n;
	scanf("%d", &n);

	node * head;
	head = NULL;

	int frnds[n];

	for (int i = 0; i < n; i++)	{
		int d;

		scanf("%d%d", &d, &frnds[i]);
		head = addnode(head, d);

	}
	addfriends(head, frnds, n);
	table t;
	t = (table) {calloc(n, sizeof(entry)), n, hasher};
	//linear probe insert
	for (node * cur = head; cur; cur = cur->next)	{
		int pos;
		int i;
		i = 0;
		pos = t.h(cur, &t);
		while ((t.tbl + pos)->original && (i++ < n))
			pos = (++pos) % n;
		*(t.tbl + pos) = (entry) {cur, malloc(sizeof(node))};
		*((t.tbl + pos)->copy) = (node) {cur->data, NULL, NULL};

	}
	//correct pointers of the copy
	for (node * cur = head; cur; cur = cur->next)	{
		node * curcopy;
		curcopy = get(t, cur);
		curcopy->next = get(t, cur->next);
		curcopy->friend = get(t, cur->friend);

	}

	for (node * cur = get(t, head); cur; cur = cur->next)
		printf("%d_", cur->friend->data);
	printf("\n");

}

node * get(table t, node * key)
{
	if(!key)
		return NULL;

	int pos;
	int i;
	i = 0;
	pos = t.h(key, &t);
	while (((t.tbl + (pos++) % t.n)->original != key) && (i++ < t.n));
	if(i == t.n)
		return NULL;
	return (t.tbl + --pos)->copy;

}

int hasher(node * key, table * t)
{
	if(!key)
		return -1;
	return (unsigned long long) key % t->n;

}

node * addnode(node * head, int d)
{
	node * cur;
	node * new;
	new = malloc(sizeof(struct node));
	*new = (node) {d, NULL, NULL};
	if(!head)
		return new;

	for(cur = head; cur->next; cur = cur->next);
	cur->next = new;
	return head;

}

void addfriends(node * head, int friends[], int n)
{
	node * cur;
	cur = head;

	for (int i = 0; i < n; i++, cur = cur->next)	{
		int j;
		j = 1;
		
		node * cur2;

		for (cur2 = head; j < friends[i]; j++, cur2 = cur2->next);
		cur->friend = cur2;

	}

}
