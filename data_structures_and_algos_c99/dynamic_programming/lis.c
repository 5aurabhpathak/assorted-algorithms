#include <stdio.h>
#include <stdlib.h>

struct tuplelist 	{
	long l;
	struct tuplelist * next;
};

struct List 	{
	struct tuplelist * l;
	struct List * next;
	unsigned long size;
} *list = NULL;

void add(long);
void display(struct List *);
void displaytl(struct tuplelist *);
struct List * copy(struct List *);

int main()
{
	unsigned long n;
	scanf("%lu", &n);
	for (unsigned long i = 0; i < n; i++) 	{
		long ai;
		scanf("%ld", &ai);
		add(ai);
	}
	unsigned long max = 0;
	//display(list);
	for (struct List * cur = list; cur; cur = cur->next)
		if (cur->size > max)
			max = cur->size;
	printf("%lu\n", max);
}

void add(long e)
{
	if (!list) 	{
		struct List * new = malloc(sizeof(struct List));
		*new = (struct List) {malloc(sizeof(struct tuplelist)), NULL, 1};
		*(new->l) = (struct tuplelist) {e, NULL};
		list = new;
		return;
	}
	unsigned long maxsize = 0;
	struct List * t = NULL;
	unsigned char flag = 0;
	//display(list);
	for (struct List * cur = list; cur; cur = cur->next) 	{
		if ((cur->l->l < e) && (cur->size > maxsize)) 	{
			maxsize = cur->size;
			t = cur;
		}
		else if (cur->l->l >= e)
			flag = 1;
	}
	if (t) 	{
		struct List * tcopy = copy(t);
		struct tuplelist * new = malloc(sizeof(struct tuplelist));
		*new  = (struct tuplelist) {e, tcopy->l};
		tcopy->l = new;
		//displaytl(t->l);
		if (flag)
			for (struct List * cur = list, *prev = NULL; cur; cur = cur->next)
				if (cur->size == tcopy->size)
					if (prev)
						prev->next = cur->next;
					else
						list = cur->next;
				else prev = cur;
		tcopy->next = list;
		list = tcopy;
	}
	else 	{
		t = malloc(sizeof(struct List));
		*t = (struct List) {malloc(sizeof(struct tuplelist)), list, 1};
		*(t->l) = (struct tuplelist) {e, NULL};
		list = t;
	}
}

void display(struct List * l)
{
	printf("Displaying all sequences...\n");
	for (struct List * c = l; c; c = c->next) 	{
		printf("length: %lu\n", c->size);
		displaytl(c->l);
	}
}

void displaytl(struct tuplelist * l)
{
	for (struct tuplelist * cur = l; cur; cur = cur->next)
		printf("%ld,\t", cur->l);
	printf("\n");
}

struct List * copy(struct List * orig)
{
	struct List * cp = malloc(sizeof(struct List));
	*cp = (struct List) {NULL, NULL, orig->size+1};
	for (struct tuplelist * cur = orig->l; cur; cur = cur->next) 	{
		struct tuplelist * new = malloc(sizeof(struct tuplelist));
		*new = (struct tuplelist) {cur->l, cp->l};
		cp->l = new;
	}
	return cp;
}
