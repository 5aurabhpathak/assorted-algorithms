#include <stdio.h>
#include <stdlib.h>

typedef struct tn	{
	struct tn * parent;
	struct tn * left;
	int key;
	struct tn * right;
} treenode;

treenode * insert(int, treenode *, treenode *);
treenode * lca(int, int, treenode *);
int search(int, treenode *);

int main()
{
	int n;
	scanf("%d", &n);

	treenode * t;
	t = NULL;
	for (int i = 0; i < n; i++)	{
		int key;
		scanf("%d", &key);
		t = insert(key, t, NULL);
	}

	int m;
	scanf("%d%d", &n, &m);
	treenode * lcanode;
	lcanode = lca(n, m, t);
	printf("%d\n", lcanode ? lcanode->key : -1);
	return 0;
}

treenode * insert(int key, treenode * t, treenode * p)
{
	treenode * new;
	new = malloc(sizeof(treenode));
	*new = (treenode) {p, NULL, key, NULL};

	if (!t)
		return new;

	if (key < t->key)
		t->left = insert(key, t->left, t);
	else
		t->right = insert(key, t->right, t);

	return t;
}

treenode * lca(int n, int m, treenode * t)
{
	if (!t)
		return NULL;
	if ((n < t->key) && (m < t->key))
		return lca(n, m, t->left);
	else if ((n > t->key) && (m > t->key))
		return lca(n, m, t->right);

	//one is less and other is big. we just dont know which so...
	if ((n < t->key) && (m > t->key))	{
		if (search(n, t->left) && search(m, t->right))
			return t;
		else return NULL;
	}
	else if ((m < t->key) &&(n > t->key))	{
		if (search(m, t->left) && search(n, t->right))
			return t;
		else return NULL;
	}
	else if (n == t->key)	{
		if (m < t->key)	{
			if (search(m, t->left))
				return t;
			else return NULL;
		}
		else if (m > t->key)	{
			if (search(m , t->right))
				return t;
			else return NULL;
		}
	}
	else if (m == t->key)	{
		if (n < t->key)	{
			if (search(n, t->left))
				return t;
			else return NULL;
		}
		else if (n > t->key)	{
			if (search(n , t->right))
				return t;
			else return NULL;
		}
	}
}

int search(int key, treenode * t)
{
	if (!t)
		return 0;

	if (t->key == key)
		return 1;
	else if (key < t->key)
		return search(key, t->left);
	else return search(key, t->right);
}
