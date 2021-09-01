#include <stdio.h>
#include <stdlib.h>

typedef struct node	{
	struct node * left;
	int key;
	struct node * right;
	struct node * parent;
} node;

node * construct(int[], int [], int, int, int, int, node *);
void preorder(node *);

int main()
{
	int n;
	scanf("%d", &n);
	int in[n];
	int post[n];
	node * root;
	root = NULL;
	for (int i = 0; i < n; i++)
		scanf("%d", &in[i]);

	for (int i = 0; i < n; i++)
		scanf("%d", &post[i]);
	root = construct(post, in, 0, n, 0, n, NULL);
	preorder(root);
	printf("\n");

	return 0;

}

node * construct(int post[], int in[], int beg, int end, int pbeg, int pend, node * parent)
{
	if (beg == end)
		return NULL;
	node * new;
	new = malloc(sizeof(node));
	*new = (node) {NULL, post[pend - 1], NULL, parent};
	
	int i;
	for (i = beg; i < end; i++)
		if (in[i] == post[pend - 1])
			break;

	new->left = construct(post, in, beg, i, pbeg, pbeg + i - beg, new);
	new->right = construct(post, in, i + 1, end, pbeg + i - beg, pend - 1, new);

	return new;

}

void preorder(node * root)
{
	if(!root)
		return;
	printf("%d_", root->key);
	preorder(root->left);
	preorder(root->right);

}
