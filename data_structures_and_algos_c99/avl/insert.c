#include <stdio.h>
#include <stdlib.h>

#define max(a, b) ((a > b) ? a : b)

struct treenode	{
	struct treenode *left;
	int key;
	int height;
	struct treenode *right;
	struct treenode *parent;
};

struct treenode * insert(struct treenode *, int, struct treenode *);
void preorder(struct treenode *);
struct treenode * rightrotate(struct treenode *);
struct treenode * leftrotate(struct treenode *);
int height(struct treenode *);

int main()
{
	int t;
	scanf("%d", &t);

	for (int i = 0; i < t; i++)	{
		int n;
		scanf("%d", &n);

		struct treenode *root;
		root = NULL;
		for(int i = 0; i < n; i++)	{
			int key;
			scanf("%d", &key);
			root = insert(root, key, NULL);
		}

		preorder(root);
		printf("\n");
		free(root);
	}
}

struct treenode * insert(struct treenode *root, int key, struct treenode *parent)
{
	static int balanced = 0;
	if (!root)	{
		struct treenode *new = malloc(sizeof(struct treenode));
		*new = (struct treenode) {NULL, key, 1, NULL, parent};
		balanced = 0;
		return new;
	}

	if (key < root->key)
		root->left = insert(root->left, key, root);
	else
		root->right = insert(root->right, key, root);

	root->height = max(height(root->left), height(root->right)) + 1;
	if (!balanced)	{
		int bal;
		bal = height(root->left) - height(root->right);
		if (bal > 1)	{
			if (key >= root->left->key)
				root->left = leftrotate(root->left);
			root = rightrotate(root);
			balanced = 1;
		}
		else if (bal < -1)	{
			if (key < root->right->key)
				root->right = rightrotate(root->right);
			root = leftrotate(root);
			balanced = 1;
		}
	}
	return root;
}

void preorder(struct treenode *root)
{
	if (!root)
		return;

	printf("%d ", root->key);
	preorder(root->left);
	preorder(root->right);
}

struct treenode * rightrotate(struct treenode *root)
{
	if (!root || !root->left)
		return root;

	struct treenode *newroot = root->left;
	struct treenode *tmp = newroot->right;
	newroot->right = root;
	root->parent = newroot;
	root->left = tmp;
	if (tmp)
		tmp->parent = root;
	newroot->parent = NULL;
	newroot->height = max(height(newroot->left), height(newroot->right)) + 1;
	root->height = max(height(root->left), height(root->right)) + 1;
	return newroot;
}

struct treenode * leftrotate(struct treenode *root)
{
	if (!root || !root->right)
		return root;

	struct treenode *newroot = root->right;
	struct treenode *tmp = newroot->left;
	newroot->left = root;
	root->parent = newroot;
	root->right = tmp;
	if (tmp)
		tmp->parent = root;
	newroot->parent = NULL;
	newroot->height = max(height(newroot->left), height(newroot->right)) + 1;
	root->height = max(height(root->left), height(root->right)) + 1;
	return newroot;
}

int height(struct treenode *root)
{
	if (!root)
		return 0;

	return root->height;
}
