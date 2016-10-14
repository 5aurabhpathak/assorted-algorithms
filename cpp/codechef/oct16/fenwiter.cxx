#include <bitset>
#include <iostream>
#include <string>
using namespace std;

bitset<1000> l1, l2, l3;
int n, p, q, r, off;
long cnt;

bool zero(bitset<1000> &b, int s)
{
	int i = -1;
	while (++i < s && b.test(i));
	if (i == s) return false;
	off = i + 1;
	return true;
}

long count_one(bitset<1000> &b, int o, int s)
{
	int i = o-1;
	long res = 0l;
	while (++i < s) res += b.test(i);
	return res;
}

void find()
{
	if (!zero(l3, r)) {
		if (!zero(l2, q)) {
			if(!zero(l1, p)) return;
			cnt += count_one(l1, off, p);
		}
		else cnt += count_one(l2, off, q) + (--n) * count_one(l2, 0, q) + count_one(l1, 0, p);
	}
	else cnt += count_one(l3, off, r) + n * count_one(l2, 0, q) + count_one(l1, 0, p);
}

int main()
{
	ios_base::sync_with_stdio(false);
	int t;
	string a, b, c;
	cin >> t;
	while (t--) {
		cnt = 1l;
		cin >> a >> b >> c >> n;
		p = a.size();
		q = b.size();
		r = c.size();
		l1 = bitset<1000>(a);
		l2 = bitset<1000>(b);
		l3 = bitset<1000>(c);
		find();
		cout << cnt << endl;
	}
}
