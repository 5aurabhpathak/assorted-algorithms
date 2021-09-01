/*
*This program uses dynamically growing and shrinking stack
*to exactlly simulate the output of the heap implemented
*through arrays as required by assignment. This is the reason
*of it being a large program as dynamic stack routines need
*to be written.(100+ extra LOC)
*In general, however, we dont need such a data structure
*to make a heap using binary trees but output would be different
*from the one which uses arrays as implementation method.
*PS: Using binary trees to implement heap is a bad idea,
*asymptotically speaking. ;)
*/
#include <stdio.h>
#include <stdlib.h>

struct treenode	{
	struct treenode * left;
	int key;
	struct treenode * right;
	struct treenode * parent;
};

struct minheap	{
	struct treenode * root;
	struct treenode * last;
	int size;
	int capacity;
};

struct dynamicstack	{
	struct treenode **a;
	int top;
	int capacity;
} s = {NULL, 0, 0};

void insert(struct treenode *, struct minheap *);
void deletemin(struct minheap *);
void heapify(struct treenode *);
int checkfull(struct minheap *);
int checkempty(struct minheap *);
void display(struct dynamicstack *);
void push(struct dynamicstack *, struct treenode *);
struct treenode * pop(struct dynamicstack *);
void enlarge(struct dynamicstack *);
void shrink(struct dynamicstack *);
int indexof(struct dynamicstack *, struct treenode *);

int main()
{
	int n;
	scanf("%d", &n);

	struct minheap t;
	t = (struct minheap) {NULL, NULL, 0, n};
	int c;
	while (scanf("%d", &c) > 0)	{
		int key;
		switch (c)	{
		case 1:
			if (checkfull(&t))	{
				printf("overflow\n");
				break;
			}
			scanf("%d", &key);
			struct treenode * new;
			new = malloc(sizeof(struct treenode));
			*new = (struct treenode) {NULL, key, NULL, NULL};
			insert(new, &t);
			display(&s);
			break;
		case 2:
			if (checkempty(&t))	{
				printf("underflow\n");
				break;
			}
			deletemin(&t);
			display(&s);
			break;
		case 3:
			printf("%s\n", checkfull(&t) ? "true" : "false");
			break;
		case 4:
			printf("%s\n", checkempty(&t) ? "true" : "false");
			break;
		case 5:
			return 0;
		default:
			return 1;
		}
	}		
}

void insert(struct treenode *new, struct minheap * t)
{
	push(&s, new);
	if (!t->root)	{
		t->size++;
		t->last = t->root = new;
		return;
	}

	new->parent = t->last;
	if (!t->last->left)	{
		t->last->left = new;
	}
	else	{
		t->last->right = new;
		t->last = s.a[indexof(&s, t->last) + 1];
	}
	t->size++;

	while (new->parent && (new->parent->key > new->key))	{
		int tmp;
		tmp = new->key;
		new->key = new->parent->key;
		new->parent->key = tmp;
		new = new->parent;
	}
}

void deletemin(struct minheap *t)
{
	struct treenode *ret;
	ret = pop(&s);

	if (ret == t->root)
		t->root = NULL;
	else
		t->root->key = ret->key;

	t->last = ret->parent;
	free(ret);
	heapify(t->root);
	t->size--;
}

void heapify(struct treenode *root)
{
	if (!root)
		return;

	int smallest;
	smallest = root->key;
	struct treenode * index;
	index = NULL;
	if (root->left && (root->left->key < smallest))	{
		smallest = root->left->key;
		index = root->left;
	}
	if (root->right && (root->right->key < smallest))	{
		smallest = root->right->key;
		index = root->right;
	}

	if (index)	{
		index->key = root->key;
		root->key = smallest;
		heapify(index);
	}
}

int checkfull(struct minheap *heap)
{
	if (heap->size == heap->capacity)
		return 1;
	return 0;
}

int checkempty(struct minheap *heap)
{
	if (!heap->size)
		return 1;
	return 0;
}

int indexof(struct dynamicstack *s, struct treenode *key)
{
	if (!key || !s)
		return -1;

	for (int i = 0; i < s->top; i++)
		if (s->a[i] == key)
			return i;
	return -1;
}

void display(struct dynamicstack *s)
{
	if (!s->top)	{
		printf("Empty\n");
		return;
	}

	struct treenode *cur;
	int i;
	for (cur = s->a[0], i = 0; i < s->top; i++, cur = s->a[i])
		printf("%d ", cur->key);
	printf("\n");
}

void push(struct dynamicstack *s, struct treenode *node)
{
	if (s->top == s->capacity)
		enlarge(s);
	s->a[s->top++] = node;
}

struct treenode * pop(struct dynamicstack *s)
{
	if (!s->top)
		return NULL;

	struct treenode *ret;
	ret = s->a[--s->top];
	if ((s->top > 0) && (s->top == s->capacity / 4))
		shrink(s);

	if (ret->parent && (ret->parent->left == ret))
		ret->parent->left = NULL;
	else if (ret->parent)
		ret->parent->right = NULL;
	return ret;
}

void enlarge(struct dynamicstack *s)
{
	if (!s->a)	{
		s->a = malloc(sizeof(struct treenode *));
		s->capacity = 1;
		return;
	}

	s->capacity *= 2;
	s->a = realloc(s->a, s->capacity * sizeof(struct treenode *));
}

void shrink(struct dynamicstack *s)
{
	s->capacity /= 2;
	s->a = realloc(s->a, s->capacity *  sizeof(struct treenode *));
}
