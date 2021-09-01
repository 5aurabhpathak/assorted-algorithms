#include <stdio.h>
#include <stdlib.h>
typedef unsigned long long llu;

struct List 	{
	long long x, y;
	struct List * next;
} **list = NULL;

unsigned long len = 0;

void add(struct List *);
void display(struct List *);
void binarysearch(llu*, llu*, struct List *,llu*);
unsigned char listcompare(struct List *, struct List *);
inline unsigned char compare(struct List *, struct List *);

int main()
{
	unsigned long n;
	scanf("%lu", &n);
	list = calloc(n, sizeof(struct List *));
	for (unsigned long i = 0; i < n; i++) 	{
		struct List * ai = malloc(sizeof(struct List));
		scanf("%lld%lld", &(ai->x), &(ai->y));
		ai->next = NULL;
		add(ai);
	}
	printf("%lu\n", len);
}

void add(struct List * e)
{
	if (len == 0) 	{
		list[0] = e;
		len++;
		return;
	}
	unsigned long index;
	if (listcompare(list[0], e)) index = 0;
	else if (listcompare(e, list[len -1])) index = len++;
	else index = binarysearch(-1, len - 1, e);
	e->next = list[index];
	list[index] = e;
}

unsigned long binarysearch(unsigned long s, unsigned long e, struct List * key)
{
	while (e - s > 1) 	{
		unsigned long m = s + (e - s) / 2;
		if (listcompare(key, list[m]))
			s = m;
		else
			e = m;
	}
	return e;
}

unsigned char listcompare(struct List * key, struct List * head)
{
	for (struct List * cur = head; cur; cur = cur->next)
		if (compare(cur, key))
			return 1;
	return 0;
}

unsigned char compare(struct List * a, struct List * b)
{
	if ((a->x < b->x) && (a->y < b->y)) return 1;
	return 0;
}

void display(struct List * l)
{
	printf("Displaying all sequences...\n");
	for (struct List * c = l; c; c = c->next)
		printf("Leader: (%lld, %lld)\n", c->x, c->y);
}
