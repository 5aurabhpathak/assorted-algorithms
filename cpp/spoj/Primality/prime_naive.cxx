#include <iostream>
int main()
{
	using std::cout;
       	using std::cin;
	using std::endl;
	int t, m, n;
	bool flag;
	cin >> t;

	for (int i = 0; i < t; i++)
	{
		cin >> m >> n;
		if (m <= 2)
		{
			cout << 2 << endl;
			m = 3;
		}
		for (int j = m; j <= n; j++)
		{
			if (j % 2 == 0) continue;
			flag = true;
			for (int k = 3; k * k <= j; k += 2)
				if (j % k == 0)
				{
				       	flag = false;
					break;
				}
			if (flag) cout << j << endl;
		}
		cout << endl;
	}
}
