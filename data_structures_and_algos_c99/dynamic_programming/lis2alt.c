#include <stdio.h>
#include <stdlib.h>

struct tuple 	{
	long long x, y;
	struct tuple * left;
	struct tuple * right;
} **list = NULL;

unsigned long len = 0;

void add(struct tuple *);
void display(struct tuple *);
unsigned long binarysearch(unsigned long, unsigned long, struct tuple *);
unsigned char bstbigger(struct tuple *, struct tuple *, unsigned char);
unsigned char bstsmaller(struct tuple *, struct tuple *, unsigned char);
struct tuple * bstinsert(struct tuple *, struct tuple *);
inline unsigned char compare(struct tuple *, struct tuple *);

int main()
{
	unsigned long n;
	scanf("%lu", &n);
	list = calloc(n, sizeof(struct tuple *));
	for (unsigned long i = 0; i < n; i++) 	{
		struct tuple * ai = malloc(sizeof(struct tuple));
		scanf("%lld%lld", &(ai->x), &(ai->y));
		ai->left = ai->right = NULL;
		add(ai);
		//for (unsigned long j = 0; j < len; j++) 	{
		//	printf("bst at %lu:\t", j);
		//	display(list[j]);
		//}
		//printf("done\n");
	}
	printf("%lu\n", len);
}

void add(struct tuple * e)
{
	if (len == 0) 	{
		list[0] = e;
		len++;
		return;
	}
	unsigned long index;
	if (bstsmaller(e, list[0], 1) != 2) index = 0;
	else if (bstbigger(e, list[len -1], 1) == 1) index = len++;
	else index = binarysearch(-1, len - 1, e);
	list[index] = bstinsert(e, list[index]);
}

unsigned long binarysearch(unsigned long s, unsigned long e, struct tuple * key)
{
	while (e - s > 1) 	{
		unsigned long m = s + (e - s) / 2ul;
		if (bstbigger(key, list[m], 1) == 1)
			s = m;
		else
			e = m;
	}
	return e;
}

unsigned char bstbigger(struct tuple * key, struct tuple * head, unsigned char status)
{
	if (!head) return status;
	status = compare(head, key);
       	if (status == 1) return status;
	return bstbigger(key, head->left, status);
}

unsigned char bstsmaller(struct tuple * key, struct tuple * head, unsigned char status)
{
	if (!head) return status;
	status = compare(key, head);
       	if (status == 1) return status;
	return bstsmaller(key, head->right, status);
}

unsigned char compare(struct tuple * a, struct tuple * b)
{
	if ((a->x < b->x) && (a->y < b->y)) return 1;
	if ((a->x > b->x) && (a->y > b->y)) return 2;
	return 0;
}

struct tuple * bstinsert(struct tuple * key, struct tuple * root)
{
	if (!root) return key;
	if ((key->x < root->x) && (key->y < root->y))	{
		key->left = root->left;
		key->right = root->right;
		root = key;
	}
	else if ((key->x > root->x) || (((key->x == root->x) && (key->y > root->y)))) root->right = bstinsert(key, root->right);
	else root->left = bstinsert(key, root->left);
	return root;
}

void display(struct tuple * l)
{
	if (!l) return;
	display(l->left);
	printf("Leader: (%lld, %lld)\n", l->x, l->y);
	display(l->right);
}
