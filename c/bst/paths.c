#include <stdio.h>
#include <stdlib.h>

typedef struct node	{
	struct node * left;
	int key;
	struct node * right;
	struct node * parent;
} node;

node * insert(int, node *, node *);
void printpaths(node *);
void printparents(node *);

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
	printpaths(root);

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

void printpaths(node * root)
{
	if(!root)
		return;

	if(!root->left && !root->right)	{
		printparents(root);
		printf("\n");

	}

	printpaths(root->left);
	printpaths(root->right);

}

void printparents(node * leaf)
{
	if(!leaf)
		return;
	printparents(leaf->parent);
	printf("%d_", leaf->key);

}
