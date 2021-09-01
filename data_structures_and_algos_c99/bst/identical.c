#include <stdio.h>
#include <stdlib.h>

typedef struct node	{
	struct node * left;
	int key;
	struct node * right;
	struct node * parent;
} node;

node * insert(int, node *, node *);
int compare(node *, node *);

int main()
{
	int t;
	int n;
	scanf("%d%d", &t, &n);

	for(int j = 0; j < t; j++)	{
		node * root1;
		node * root2;
		root1 = NULL;
		root2 = NULL;
	
		for (int i = 0; i < 2 * n; i++)	{
			int data;
			scanf("%d", &data);
			if(i < n)
				root1 = insert(data, root1, NULL);
			else
				root2 = insert(data, root2, NULL);

		}

		if(compare(root1, root2))
			printf("y\n");
		else
			printf("n\n");

	}

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

int compare(node * root1, node * root2)
{
	if(root1 && !root2)
		return 0;
	if(!root1 && root2)
		return 0;
	if(!root1 && !root2)
		return 1;
	if(root1->key != root2->key)
		return 0;
	if(!compare(root1->left, root2->left))
		return 0;
	if(!compare(root1->right, root2->right))
		return 0;
	return 1;

}
