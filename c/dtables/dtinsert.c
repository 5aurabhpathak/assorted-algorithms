#include <stdio.h>
#include <stdlib.h>

typedef struct node {
	int *a;
	int capacity;
	int size;

} head;

void insert(head *, int);
void display(head *);
void push_back(head *, int);

void main()
{
	head * dt;

	dt = malloc(sizeof(head));

	int n;

	scanf("%d", &n);
	*dt = (head){malloc(sizeof(int)), 1, 0};
	for (int i = 0; i < n; i++)	{
		int data;

		scanf("%d", &data);
		insert(dt, data);
		display(dt);

	}

}

void insert(head * dt, int data)
{
	//resize if the case
	if(dt->capacity == dt->size)	{
		int * tmp;

		dt->capacity = 2*dt->capacity;
		while(!(tmp = realloc(dt->a, dt->capacity*sizeof(int))));
		dt->a = tmp;

	}
	push_back(dt, data);

}

void push_back(head * dt, int data)
{
	//push back at the end
	int *pos;
	
	pos = dt->a + dt->size;
	*pos = data;
	dt->size++;

}

void display(head *dt)
{
	printf("capacity = %d; size = %d; elements = ", dt->capacity, dt->size);
	for(int i = 0; i < dt->size; i++)	{
		//iterate
		printf("%d ", *(dt->a + i));
	}
	printf("\n");

}
