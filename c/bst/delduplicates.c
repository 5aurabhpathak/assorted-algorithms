#include <stdio.h>
#include <stdlib.h>

typedef struct node	{
	struct node * left;
	int key;
	struct node * right;
	struct node * parent;
} node;

node * insert(node *, node *, node *);
node * deleteduplicates(node *);
node * delete(int, node *);
node * deleteroot(node *);
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

	root = deleteduplicates(root);
	inorder(root);
	printf("\n");

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

node * deleteduplicates(node * root)
{
	//traverse in preorder
	if (!root)
		return NULL;
	//delete duplicates of this key. BST means duplicates if any
	//would be in the right subtree, so...
	root->right = delete(root->key, root->right);
	root->left = deleteduplicates(root->left);
	root->right = deleteduplicates(root->right);
	return root;

}

node * delete(int key, node * root)
{
	//delete all keys in this tree with value = key
	if (!root)
		return NULL;
	//if root = key and has a right child then delete root and search the resulting tree
	//coz more duplicates may be present
	//else our key is smaller and search the left subtree
	//note that since key came from a predecessor of this tree it will not
	//be larger than this root
	//if root = key and no right child then our work is done after deleteing root!
	if (key == root->key)
		if (root->right)
			root = delete(key, deleteroot(root));
		else
			root = deleteroot(root);
	else
		root->left = delete(key, root->left);
	return root;

}

node * deleteroot(node * root)
{
	if (!root->right && !root->left)
		return NULL;
	//aim is to make right child the newroot. If none, then left child is chosen.
	node * newroot;
	newroot = root->right ? root->right : root->left;
	newroot->parent = root->parent;
	//correct pointers of the parent node, if exixts, to point to our new root.
	if (root->parent)
		if(root->parent->left == root)
			root->parent->left = newroot;
		else
			root->parent->right = newroot;
	//did we choose the left child? then happy..
	if (!root->right)
		return newroot;
	//else more work! :( left child of our newroot needs to be adjusted
	node * tmp;
	tmp = newroot->left;
	newroot->left = root->left;
	free(root);
	//or was there none?
	if (tmp)
		return insert(tmp, newroot->left, newroot);
	return newroot;

}

void inorder(node * root)
{
	if(!root)
		return;
	inorder(root->left);
	printf("%d_", root->key);
	inorder(root->right);

}
