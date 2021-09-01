#include <stdio.h>
#include <stdlib.h>

#define INITIAL_TABLE_SIZE 10
#define HASHTABLE_SIZE 10

typedef struct node {
	int data;
	struct node * next;
	struct node * leader;
} node;

typedef struct ds {
	node * leader;
	node * tail;
	int size;
} disjointset;

void makeset(node *);
void dounion(disjointset *, disjointset *);
void append(disjointset *, disjointset *);
int search(disjointset *);
disjointset * find(node *);
node * getnode(int key);
void insert(int, node *);
void resize();
void displaysets();
void displayset(disjointset *);
void displaynodes();

typedef struct sets {
	disjointset ** a;
	int size;
	int capacity;
} dynamictable;
dynamictable all;

typedef struct cn {
	int key;
	node * value;
	struct cn * next;
} chainnode;

typedef struct ht {
	chainnode ** a;
	int size;
	int capacity;
} hashtable;
hashtable ht;

#define hash(a) a % ht.capacity;

chainnode * addnode(chainnode *, int, node *);

int main()
{
	int choice;
	all = (dynamictable) {calloc(INITIAL_TABLE_SIZE, sizeof(disjointset *)), 0, INITIAL_TABLE_SIZE};
	ht = (hashtable) {calloc(HASHTABLE_SIZE, sizeof(node *)), 0, HASHTABLE_SIZE};

	while (scanf("%d", &choice) > 0)	{
		int data;
		int leader1;
		int leader2;
		switch (choice)	{
		case 1:
			scanf("%d", &data);
			node * new;
			new = malloc(sizeof(node));
			*new = (node) {data, NULL, new};
			makeset(new);
			printf("Set %d added\n", data);
			displaynodes();
			displaysets();
			break;

		case 2:
			scanf("%d%d", &leader1, &leader2);
			dounion(find(getnode(leader1)), find(getnode(leader2)));
			printf("%d union %d\n", leader1, leader2);
			displaynodes();
			displaysets();
			break;

		case 3:
			scanf("%d", &data);
			printf("%s\n", find(getnode(data)) ? "found" : "not found");
			break;

		default:
			return 0;
		}
	}
}

void resize()
{
	all.capacity *= 2;
	all.a = realloc(all.a, all.capacity * sizeof(disjointset *));
}

void makeset(node * leader)
{
	disjointset * new;
	new = malloc(sizeof(disjointset));
	*new = (disjointset) {leader, leader, 1};
	if (all.size == all.capacity)
		resize();
	all.a[all.size] = new;
	all.size++;
	insert(leader->data, leader);
}

void insert(int key, node * value)
{
	int loc;
	loc = hash(key);
	ht.a[loc] = addnode(ht.a[loc], key, value);
	ht.size++;
}

chainnode * addnode(chainnode * c, int key, node * value)
{
	chainnode * new;
	new = malloc(sizeof(chainnode));
	*new = (chainnode) {key, value, c};
	return new;
}

void dounion(disjointset * x, disjointset * y)
{
	if ((!x) || (!y))
		return;

	if (x->size < y->size)
		append(y, x);
	else
		append(x, y);
}

void append(disjointset * x, disjointset * y)
{
	x->tail->next = y->leader;
	for (node * cur = y->leader; cur; cur = cur->next)
		cur->leader = x->leader;
	x->tail = y->tail;
	x->size += y->size;
	all.size--;
	all.a[search(y)] = all.a[all.size];
}

int search(disjointset * k)
{
	for (int i = 0; i < all.size; i++)
		if(all.a[i] == k)
			return i;
	return -1;
}

disjointset * find(node * key)
{
	if (!key)
		return NULL;

	for (int i = 0; i < all.size; i++)
		if(all.a[i]->leader == key->leader)
			return all.a[i];
	return NULL;
}

node * getnode(int key)
{
	int loc;
	loc = hash(key);
	
	//search chain at loc
	chainnode * c;
	c = ht.a[loc];
	while(c)	{
		if(c->key == key)
			return c->value;
		c = c->next;
	}
	return NULL;
}

void displaysets()
{
	printf("All sets:\n");
	for (int i = 0; i < all.size; i++)
		displayset(all.a[i]);
}

void displayset(disjointset * d)
{
	node * cur;
	cur = d->leader;
	for (int i = 0; i < d->size; i++, cur = cur->next)
		printf("%d ", cur->data);
	printf("\n");
}

void displaynodes()
{
	printf("Nodes table:\n");
	for (int i = 0, j = 0; i < ht.capacity && j < ht.size; i++)	{
		for (chainnode * cur = ht.a[i]; cur; cur = cur->next, j++)
			printf("%d ", cur->key);
		printf("\n");
	}
}
