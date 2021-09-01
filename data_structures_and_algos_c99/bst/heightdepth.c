#include <stdio.h>
#include <stdlib.h>

#define max(a, b) (a > b ? a : b)

typedef struct node	{
	struct node * left;
	int key;
	struct node * right;
	struct node * parent;
} node;

node * insert(int, node *, node *);
void preorder(node *, int, int);
int height(node *);

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

	preorder(root, height(root), 0);

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

void preorder(node * root, int h, int d)
{
	if(!root)
		return;
	printf("node: %d\theight: %d\tdepth: %d\n", root->key, h, d);
	preorder(root->left, h - 1, d + 1);
	preorder(root->right, h - 1, d + 1);

}

int height(node * root)
{
	if (!root)
		return -1;
	return max(height(root->left), height(root->right)) + 1;

}
