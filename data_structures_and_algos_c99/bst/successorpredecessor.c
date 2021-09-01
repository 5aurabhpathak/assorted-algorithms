#include <stdio.h>
#include <stdlib.h>

typedef struct node	{
	struct node * left;
	int key;
	struct node * right;
	struct node * parent;
} node;

node * insert(int, node *, node *);
node * getsuccessor(int, node *, node *);
node * getpredecessor(int, node *, node *);

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
	node * successor;
	successor = getsuccessor(n, root, NULL);
	node * predecessor;
	predecessor = getpredecessor(n, root, NULL);
	printf("%d\t%d\n", successor ? successor->key : -1, predecessor ? predecessor->key : -1);

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

//pred is the predecessor of the current(root) node if it had no left child
node * getpredecessor(int key, node * root, node * pred)
{
	if (root->key == key)	{
		if (root->left)
			return root->left;
		else return pred;
	}
	if (key < root->key)
		return getpredecessor(key, root->left, pred);
	else
		return getpredecessor(key, root->right, root);

}

node * getsuccessor(int key, node * root, node * suc)
{
	if(root->key == key)	{
		if (root->right)
			return root->right;
		else return suc;
	}
	if (key < root->key)
		return getsuccessor(key, root->left, root);
	else
		return getsuccessor(key, root->right, suc);

}
