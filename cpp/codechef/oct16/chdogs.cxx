#include <cstdio>
using namespace std;

int main()
{
	int t;
	double s, v;
	scanf("%d", &t);
	while (t--) {
		scanf("%lf%lf", &s, &v);
		printf("%f\n", (2 * s) / (3 * v));
	}
}
