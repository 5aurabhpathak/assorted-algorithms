#include <stdio.h>

struct tuple 	{
	long long x,y;
};

inline unsigned char smaller(struct tuple, struct tuple);

int main()
{
	unsigned long n, globalmax = 0;
	scanf("%lu", &n);
	struct tuple arr[n];
	unsigned long mem[n];
	for (unsigned long i = 0; i < n; i++) 	{
		scanf("%lld%lld", &(arr[i].x), &(arr[i].y));
		mem[i] = 1;
		unsigned long max = 0;
		for (unsigned long j = 0; j < i; j++)
			if (smaller(arr[j], arr[i]) && (mem[j] > max))
				max = mem[j];
		mem[i] += max;
		if (mem[i] > globalmax)
			globalmax = mem[i];
	}
	printf("%lu\n", globalmax);
}

unsigned char smaller(struct tuple a, struct tuple b)
{
	if ((a.x < b.x) && (a.y < b.y)) return 1;
	return 0;
}
