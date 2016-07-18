#include <iostream>
#include <climits>

int apples(int[], int[], int, int, int[]);
using namespace std;

int main()
{
	int t, N, K;
	cin >> t;
	for (int m = 0; m < t; m++)
	{
		cin >> N >> K;
		int j = 0;
		int *v = new int[K];
		int *w = new int[K];
		int *a = new int[K]{};
		for (int i = 0; i < K; i++)
		{
			int val;
			cin >> val;
			if (val != -1)
			{
				w[j] = i + 1;
				v[j] = val;
				j++;
			}
		}
		cout << apples(w, v, j, K, a) << endl;
	}
}

int apples(int w[], int v[], int s, int k, int a[])
{
	if (k < 0)
		return -1;
	if (!k)
		return 0;
	if (a[k-1]) return a[k-1];
	int min = INT_MAX;
	for (int i = 0; i < s; i++)
	{
		int val = apples(w, v, s, k - w[i], a);
		int x = val + v[i];
		if ((val != -1) && (x < min))
			min = x;
	}
	if (min == INT_MAX)
		return -1;
	return a[k-1] = min;
}
