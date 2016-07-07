#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#define max(a, b) (a > b ? a : b)

typedef struct node	{
	struct node * left;
	int key;
	struct node * right;
	struct node * parent;
} node;

int height(node *);
node * insert(int, node *, node *);
node * trim(int, node *, int);
void inorder(node *);

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

	scanf("%d", &n);
	root = trim(n, root, 0);
	inorder(root);
	printf("\n");

	return 0;

}

int height(node * root)
{
	if (!root)
		return -1;
	return max(height(root->left), height(root->right)) + 1;

}

node * insert(int key, node * root, node * parent)
{
	if (!root)	{
		node * new;
		new = malloc(sizeof(node));
		*new = (node) {NULL, key, NULL, parent};
		return new;

	}
	if (height(root->left) < height(root->right))
		root->left = insert(key, root->left, root);
	else
		root->right = insert(key, root->right, root);

	return root;

}

node * trim(int k, node * root, int sum)
{
	if (!root)
		return NULL;
	root->left = trim(k, root->left, sum + root->key);
	root->right = trim(k, root->right, sum + root->key);
	if ((!root->left && !root->right) && ((sum + root->key) < k))	{
		free(root);
		root = NULL;

	}
	return root;

}

void inorder(node * root)
{
	if (!root)
		return;
	inorder(root->left);
	printf("%d_", root->key);
	inorder(root->right);

}
