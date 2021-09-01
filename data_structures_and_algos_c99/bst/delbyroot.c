#include <stdio.h>
#include <stdlib.h>

typedef struct node	{
	struct node * left;
	int key;
	struct node * right;
	struct node * parent;
} node;

node * insert(node *, node *, node *);
void delete(node *);
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
		node * new;
		new = malloc(sizeof(node));
		*new = (node) {NULL, data, NULL, NULL};
		root = insert(new, root, NULL);

	}
	delete(root);

	return 0;

}

node * insert(node * new, node * root, node * parent)
{
	if(!root)	{
		new->parent = parent;
		return new;

	}

	if (new->key < root->key)
		root->left = insert(new, root->left, root);
	else
		root->right = insert(new, root->right, root);

	return root;

}

void delete(node * root)
{
	if(!root)
		return;

	inorder(root);
	printf("\n");
	node * newroot;
	newroot = NULL;
	if (root->right)	{
		newroot = root->right;
		newroot->parent = NULL;
		if (root->left)	{
			root->left->parent = newroot;
			if(newroot->left)	{
				node * l = newroot->left;
				newroot->left = root->left;
				insert(l, newroot, NULL);

			}
			else
				newroot->left = root->left;

		}

	}
	else if (root->left)	{
		newroot = root->left;
		newroot->parent = NULL;
	}
	free(root);
	delete(newroot);

}

void inorder(node * root)
{
	if (!root)
		return;
	inorder(root->left);
	printf("%d_", root->key);
	inorder(root->right);

}
