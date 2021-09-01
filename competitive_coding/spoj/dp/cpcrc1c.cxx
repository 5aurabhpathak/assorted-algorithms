#include <cmath>
#include <cstdio>
using namespace std;

long long s[10], dp[9]{};

long long solve(long);
long long solve_f(int);
int main()
{
	long a, b;
	s[0] = 0ll;
	for (int i = 1; i < 10; i++) s[i] += i + s[i-1];
	scanf("%ld%ld", &a, &b);
	while (a != -1l) {
		printf("%lld\n", solve(b)-solve(a-1));
		scanf("%ld%ld", &a, &b);
	}
}

long long solve(long a)
{
	if (a < 1l) return 0ll;
	int i = 0, dig[10];
	long b = a, power;
	long long sum;
	do dig[i++] = b % 10;
	while (b /= 10l);
	sum = s[dig[0]];
	for (int j = i-1; j >= 1; j--) {
		power = pow(10l, j);
		sum += dig[j] * (solve_f(j) + a % power + 1) + s[dig[j]-1] * power;
		a %= power;
	}
	return sum;
}

long long solve_f(int i)
{
	if (dp[i]) return dp[i];
	if (i == 1) return dp[i] = 45ll;
	return dp[i] = 45ll * pow(10l, i-1) + 10ll * solve_f(i-1);
}
