#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

typedef struct node	{
	struct node * left;
	int key;
	struct node * right;
	struct node * parent;
} node;

node * insert(int, node *, node *);
int distancebetween(int, int, node *);
int height(int, node *);

int main()
{
	int n;
	scanf("%d", &n);

	node * root;
	root = NULL;
	
	for (int i = 0; i < n; i++)	{
		int data;
		scanf("%d", &data);
		root = insert(data, root, NULL);

	}

	int k;
	scanf("%d%d", &n, &k);
	printf("%d\n", distancebetween(n, k, root));

	return 0;

}

node * insert(int key, node * root, node * parent)
{
	if(!root)	{
		node * new;
		new = malloc(sizeof(node));
		*new = (node) {NULL, key, NULL, parent};
		return new;

	}

	if (key < root->key)
		root->left = insert(key, root->left, root);
	else
		root->right = insert(key, root->right, root);

	return root;

}

int distancebetween(int key1, int key2, node * root)
{
	if(!root)
		return INT_MIN;
	if ((key1 < root->key) && (key2 < root->key))
		return distancebetween(key1, key2, root->left);
	if ((key1 > root->key) && (key2 > root->key))
		return distancebetween(key1, key2, root->right);
	if (((key1 < root->key) && (key2 > root->key)) || ((key2 < root->key) && (key1 > root->key)))
		return height(key1, root) + height(key2, root);
	if (key1 == root->key)
		return height(key2, root);
	if (key2 == root->key)
		return height(key1, root);
		

}

int height(int key, node * root)
{
	if (!root)
		return INT_MIN / 2;
	if (root->key == key)
		return 0;
	if (root->key > key)
		return height(key, root->left) + 1;
	else
		return height(key, root->right) + 1;

}
