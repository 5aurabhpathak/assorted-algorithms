#include <stdio.h>
#include <stdlib.h>

typedef struct rows	{
	int *array;
	int size, used;
} row;

int search(int, int *, int);
void insert(row *, int);

int main()	{
	int n, i, j;
	scanf("%d", &n);
	int a[n][n];
	for(i = 0; i < n; i++)
		for(j = 0; j < n; j++)
			scanf("%d", &a[i][j]);

	row **uniqrow = (row **) malloc(n*sizeof(row *));
	row **uniqcol = (row **) malloc(n*sizeof(row *));
	row matr = {(int *) malloc(sizeof(int)), 1, 0};
	for(i = 0; i < n; i++)	{
		row * newrow = (row *) malloc(sizeof(row *));
		*newrow = (row){(int *) malloc(sizeof(int)), 1, 0};
		row * newcol = (row *) malloc(sizeof(row *));
		*newcol = (row){(int *) malloc(sizeof(int)), 1, 0};
		*(uniqrow+i) = newrow;
		*(uniqcol+i) = newcol;
		for(j = 0; j < n; j++)	{
			if(!search(a[i][j], newrow->array, newrow->used))	{
				if(newrow->size == newrow->used)	{
					newrow->size *= 2;
					newrow->array = (int *) realloc(newrow->array, newrow->size*sizeof(int));
				}
				insert(newrow, a[i][j]);
				newrow->used++;
			}
			
			if(!search(a[j][i], newcol->array, newcol->used))	{
				if(newcol->size == newcol->used)	{
					newcol->size *= 2;
					newcol->array = (int *) realloc(newcol->array, newcol->size*sizeof(int));
				}
				insert(newcol, a[j][i]);
				newcol->used++;
			}

			if(!search(a[i][j], matr.array, matr.used))	{
				if(matr.size == matr.used)	{
					matr.size *= 2;
					matr.array = (int *) realloc(matr.array, matr.size*sizeof(int));
				}
				insert(&matr, a[i][j]);
				matr.used++;
			}
		}
	}

	printf("Along rows:\n");
	for(i = 0; i < n; i++)	{
		row * cur = *(uniqrow+i);
		for(j = 0; j < cur->used; j++)
			printf("%d\t", *(cur->array+j));
		printf("\n");
	}

	printf("Along columns:\n");	
	for(i = 0; i < n; i++)	{
		row * cur = *(uniqcol+i);
		for(j = 0; j < cur->used; j++)
			printf("%d\t", *(cur->array+j));
		printf("\n");
	}

	printf("Matrix:\n");
	for(i = 0; i < matr.used; i++)
		printf("%d\t", *(matr.array+i));
	printf("\n");
	free(uniqrow);
	free(uniqcol);
	return 0;
}

int search(int value, int *arr, int end)	{
	for(int i = 0; i < end; i++)
		if(*(arr+i) == value)
			return 1;
	return 0;
}

void insert(row * r, int value)	{
	int i;
	for(i = r->used -1; i >= 0; i--)
		if(*(r->array+i)>value)
			*(r->array+i+1) = *(r->array+i);
		else break;
	*(r->array+i+1) = value;
}
