#include <stdio.h>
#include <stdlib.h>

#define max(a,b) (a > b ? a : b)

typedef struct node	{
	struct node * left;
	int key;
	struct node * right;
	struct node * parent;
} node;

node * bstinsert(int, node *, node *);
node * insert(int, node *, node *);
int isbst(node *);
int height(node *);
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
	inorder(root);
	printf("\n%s\n", isbst(root) ? "yes" : "no");

	return 0;

}

void inorder(node * root)
{
	if(!root)
		return;
	inorder(root->left);
	printf("%d_", root->key);
	inorder(root->right);

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

int height(node * root)
{
	if (!root)
		return -1;
	return max(height(root->left), height(root->right)) + 1;

}

node * bstinsert(int key, node * root, node * parent)
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

int isbst(node * root)
{
	if (!root)
		return 1;
	if (root->left && (root->left->key > root->key))
		return 0;
	if (root->right && (root->right->key < root->key))
		return 0;
	if (!(isbst(root->left) && isbst(root->right)))
		return 0;
	return 1;

}
