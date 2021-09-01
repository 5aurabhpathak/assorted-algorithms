#include <climits>
#include <cstdio>
#include <cstring>
using namespace std;

int solve(char [], int, int);
int main()
{
	char s[26];
	int i = 1;
	scanf("%s", s);
	while (strcmp(s, "bye")) {
		int l = strlen(s);
		printf("%d. %d\n", i++, solve(s, l, INT_MAX));
		scanf("%s", s);
	}
}

int solve(char s[], int n, int sum)
{
	if (!n) return 1;
	int c = 0, sm = 0;
	for (int i = n-1; i >= 0; i--)
		if ((sm += s[i]-'0') <= sum)
			c += solve(s, i, sm);
	return c;
}
