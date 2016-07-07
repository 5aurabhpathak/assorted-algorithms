#include <stdio.h>
#include <stdlib.h>

struct treenode	{
	struct treenode *left;
	int key;
	struct treenode *right;
	struct treenode *parent;
};

struct treenode * insert(struct treenode *, int, struct treenode *);
void preorder(struct treenode *);
struct treenode * rightrotate(struct treenode *);

int main()
{
	int n;
	scanf("%d", &n);

	struct treenode *root;
	root = NULL;
	for(int i = 0; i < n; i++)	{
		int key;
		scanf("%d", &key);
		root = insert(root, key, NULL);
	}

	root = rightrotate(root);
	preorder(root);
	printf("\n");
}

struct treenode * insert(struct treenode *root, int key, struct treenode *parent)
{
	if (!root)	{
		struct treenode *new = malloc(sizeof(struct treenode));
		*new = (struct treenode) {NULL, key, NULL, parent};
		return new;
	}

	if (key < root->key)
		root->left = insert(root->left, key, root);
	else
		root->right = insert(root->right, key, root);

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
	return newroot;
}
