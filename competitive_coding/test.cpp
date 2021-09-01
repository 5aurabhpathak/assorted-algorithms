#include <iostream>
#include <bitset>
using namespace std;
class A
{
	int a;
	public:
		A(int a): a(a) {}
		A operator+(const int a) const
		{
			return A(this->a+a);
		}
};

int main()
{
	A x(4);
	//A y = x-4;      //compile error: 'operator-' not defined!(python rocks here)
	bitset<16> b("0000");
	cout << b.empty() << endl;
}
