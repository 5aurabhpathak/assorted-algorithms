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
struct treenode * leftrotate(struct treenode *);

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

	root = leftrotate(root);
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
	return newroot;
}
