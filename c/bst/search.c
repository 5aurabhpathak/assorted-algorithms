#include <stdio.h>
#include <stdlib.h>

typedef struct node	{
	struct node * left;
	int key;
	struct node * right;
	struct node * parent;
} node;

node * insert(int, node *, node *);
node * search(int, node *);

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

	scanf("%d", &n);
	int keys[n];
	for (int i = 0; i < n; i++)
		scanf("%d", &keys[i]);
	for (int i = 0; i < n; i++)
		if(search(keys[i], root))
			printf("y\n");
		else
			printf("n\n");

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

node * search(int key, node * root)
{
	if(!root)
		return NULL;
	if (root->key == key)
		return root;
	else if (key < root->key)
		return search(key, root->left);
	else
		return search(key, root->right);

}
