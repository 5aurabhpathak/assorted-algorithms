#include <stdio.h>
#include <stdlib.h>

#define max(a,b) (a > b ? a : b)

typedef struct node	{
	struct node * left;
	int key;
	struct node * right;
	struct node * parent;
} node;

node * insert(int, node *, node *);
int issumtree(node *);
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
	printf("\n%s\n", issumtree(root) ? "yes" : "no");

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

int issumtree(node * root)
{
	if (!root->left && !root->right)
		return 1;
	else if (!root->left)	{
		if (root->key != root->right->key)
			return 0;
		return 1;

	}
	else if (!root->right)	{
		if (root->key != root->left->key)
			return 0;
		return 1;

	}
	if (root->key != root->left->key + root->right->key)
		return 0;
	if (!(issumtree(root->left) && issumtree(root->right)))
		return 0;
	return 1;

}
