#include <stdio.h>
#include <stdlib.h>

typedef struct node	{
	struct node * left;
	int key;
	struct node * right;
	struct node * parent;
} node;

node * insert(int, node *, node *);
void preorder(node *);
void inorder(node *);
void postorder(node *);

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

	preorder(root);
	printf("\n");
	inorder(root);
	printf("\n");
	postorder(root);
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

void preorder(node * root)
{
	if(!root)
		return;
	printf("%d_", root->key);
	preorder(root->left);
	preorder(root->right);

}

void inorder(node * root)
{
	if(!root)
		return;
	inorder(root->left);
	printf("%d_", root->key);
	inorder(root->right);

}

void postorder(node * root)
{
	if(!root)
		return;
	postorder(root->left);
	postorder(root->right);
	printf("%d_", root->key);

}
