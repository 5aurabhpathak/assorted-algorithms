#include <stdio.h>
#include <stdlib.h>

typedef struct node	{
	struct node * left;
	int key;
	struct node * right;
	struct node * parent;
} node;

typedef struct dt {
	node ** a;
	int size;
	int capacity;
	int front;
	int rear;
} dynamicqueue;

void enqueue(node *, dynamicqueue *);
node * dequeue(dynamicqueue *);
void resize(dynamicqueue *);
node * insert(int, node *, node *);
int bfs(int, dynamicqueue *);

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
	dynamicqueue queue;
	queue = (dynamicqueue) {malloc(sizeof(node *)), 0, 1, 0, 0};
	enqueue(root, &queue);
	printf("%s\n", bfs(n, &queue) ? "yes" : "no");

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

int bfs(int key, dynamicqueue * q)
{
	if (!q->size)
		return 0;
	node * current;
	current = dequeue(q);
	printf("key:%d\t", current->key);
	if (current->key == key)
		return 1;
	if (current->left)
		enqueue(current->left, q);
	if (current->right)
		enqueue(current->right, q);
	return bfs(key, q);

}

node * dequeue(dynamicqueue * q)
{
	if (!q->size)
		return NULL;
	node * returned;
	returned = *(q->a + q->front);
	q->front = ++q->front % q->capacity;
	q->size--;
	printf("%d\n", q->size);
	return returned;

}

void enqueue(node * key, dynamicqueue * q)
{
	if (q->size == q->capacity)
		resize(q);
	*(q->a + q->rear) = key;
	q->size++;
	printf("inserting key %d, size is now: %d\n", key->key, q->size);
	q->rear = ++q->rear % q->capacity;

}

void resize(dynamicqueue * q)
{
	int oldcap = q->capacity;
	printf("capacity:%d\n", q->capacity);
	q->capacity *= 2;
	node ** tmp;
	tmp = realloc(q->a, q->capacity * sizeof(node *));
	if (!tmp)
		exit(1);
	q->a = tmp;
	int i;
	int j;
 	for (i = oldcap - 1, j = q->capacity - 1; i >= q->front; i--, j--)
		*(q->a + j) = *(q->a + i);
	q->front = ++j;

}
