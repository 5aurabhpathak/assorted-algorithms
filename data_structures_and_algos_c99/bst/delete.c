#include <stdio.h>
#include <stdlib.h>

typedef struct node	{
	struct node * left;
	int key;
	struct node * right;
	struct node * parent;
} node;

node * insert(int, node *, node *);
void delleaves(node *);

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
	delleaves(root);
	printf("\n");

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

void delleaves(node * root)
{
	if(!root)
		return;

	delleaves(root->left);
	delleaves(root->right);
	if(!root->left && !root->right)	{
		if (root->parent)
			if (root->parent->left == root)
				root->parent->left = NULL;
			else
				root->parent->right = NULL;
		printf("%d_", root->key);
		free(root);
		return;

	}

}
