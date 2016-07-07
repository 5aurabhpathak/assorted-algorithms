#include <stdio.h>
#include <stdlib.h>

struct treenode {
	struct treenode *left;
	int key;
	struct treenode *right;
	struct treenode *parent;
};

struct treenode *insert(struct treenode *root, int key, struct treenode *parent);
struct treenode *splay(struct treenode *root);
void leftrotate(struct treenode *root);
void rightrotate(struct treenode *root);
void preorder(struct treenode *root);

int main()
{
	struct treenode *root = NULL;
	int n = 0;

	scanf("%d", &n);
	for (int i = 0; i < n; i++)	{
		int key = 0;
		scanf("%d", &key);
		root = insert(root, key, NULL);
	}

	scanf("%d", &n);
	for (int i = 0; i < n; i++)	{
		int key = 0;
		scanf("%d", &key);
		root = insert(root, key, NULL);
		preorder(root);
		printf("\n");
	}
}

struct treenode *insert(struct treenode *root, int key, struct treenode *parent)
{
	if (!root)	{
		struct treenode *new = malloc(sizeof(struct treenode));
		*new = (struct treenode) {.key = key, .parent = parent};
		root = new;
	}

	if (key < root->key)
		root->left = insert(root->left, key, root);
	else if (key > root->key)
		root->right = insert(root->right, key, root);
	else return splay(root);

	return root;
}

struct treenode *splay(struct treenode *node)
{
	if (!node || !node->parent)	{
		return node;
	}
	else if (!node->parent->parent)	{
		if (node->parent->left == node)
			rightrotate(node->parent);
		else
			leftrotate(node->parent);
	}
	else if (node->parent->parent->left == node->parent)	{
		if (node->parent->left == node)	{
			rightrotate(node->parent->parent);
			rightrotate(node->parent);
		}
		else	{
			leftrotate(node->parent);
			rightrotate(node->parent);
		}
	}
	else if (node->parent->right == node)	{
		leftrotate(node->parent->parent);
		leftrotate(node->parent);
	}
	else	{
		rightrotate(node->parent);
		leftrotate(node->parent);
	}
	return node;
}

void rightrotate(struct treenode *root)
{
	struct treenode *tmp = root->left;
	root->left = root->left->right;
	tmp->right = root;
	tmp->parent = root->parent;
	root->parent = tmp;	
}

void leftrotate(struct treenode *root)
{
	struct treenode *tmp = root->right;
	root->right = root->right->left;
	tmp->left = root;
	tmp->parent = root->parent;
	root->parent = tmp;	
}

void preorder(struct treenode *root)
{
	if (!root)
		return;

	printf("%d ", root->key);
	preorder(root->left);
	preorder(root->right);
}
