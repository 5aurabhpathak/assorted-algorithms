#include <stdio.h>
#include <stdlib.h>

typedef struct node	{
	struct node * left;
	int key;
	struct node * right;
	struct node * parent;
} node;

node * construct(int[], int [], int, int, int, int, node *);
void inorder(node *);

int main()
{
	int n;
	scanf("%d", &n);
	int pre[n];
	int post[n];
	node * root;
	root = NULL;
	for (int i = 0; i < n; i++)
		scanf("%d", &pre[i]);

	for (int i = 0; i < n; i++)
		scanf("%d", &post[i]);
	root = construct(post, pre, 0, n, 0, n, NULL);
	inorder(root);
	printf("\n");

	return 0;

}

node * construct(int post[], int pre[], int beg, int end, int postbeg, int postend, node * parent)
{
	node * new;
	new = malloc(sizeof(node));
	*new = (node) {NULL, pre[beg], NULL, parent};
	
	if (beg + 1 == end)
		return new;
	
	int i;
	for (i = postbeg; i < postend; i++)
		if (post[i] == pre[beg + 1])
			break;

	new->left = construct(post, pre, beg + 1, beg - postbeg + i + 2, postbeg, i + 1, new);
	new->right = construct(post, pre, beg - postbeg + i + 2, end, i + 1, postend - 1, new);
	return new;

}

void inorder(node * root)
{
	if(!root)
		return;
	inorder(root->left);
	printf("%d_", root->key);
	inorder(root->right);

}
