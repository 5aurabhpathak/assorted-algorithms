#include <iostream>
#include <set>
#include <string>
#include <sstream>
#include <unordered_map>
using namespace std;

struct Person
{
	struct Comp
	{
		bool operator()(const Person *p1, const Person *p2) const
		{
			static const less<string> s;
			return s(p1->name, p2->name);
		}
	};
	string name;
	set<Person*, Comp> kids;
	Person(string s) : name(s) {}
};

struct Out
{
	long tcost;
	int tf, ts;
	Out(long a, int b, int c): tcost(a), tf(b), ts(c) {}
	Out(): tcost(0), tf(0), ts(0) {}
};

struct Setcomp
{
	bool operator()(const set<Person*, Person::Comp> &a, const set<Person*, Person::Comp> &b) const
	{
		if (a.size() == b.size()) {
			for (auto i = a.begin(), j = b.begin(); i != a.end(); i++, j++) {
				if (*i < *j) return true;
				if (*i > *j) return false;	
			}
		}
		return false;
	}
};

struct Sethash
{
	unsigned long long operator()(const set<Person*, Person::Comp> &p) const
	{
		unsigned long long hashval = 0ull, i = 0ull;
		for (auto q: p) hashval += (unsigned long long)q << i++;
		/*for (auto q: p) cout << q->name << "\t";
		cout << "-->" << hashval << endl;*/
		return hashval;
	}
};

ostream& operator<<(ostream &o, const Out *out)
{
	return o << out->ts << " " << out->tf << " " << out->tcost;
}

int s,f;
unordered_map<set<Person*, Person::Comp>, Out*, Sethash, Setcomp> m;

Out* minimum(set<Person*, Person::Comp>);
int main()
{
	int ts, tf, i = 1;
	string str;
	set<Person*, Person::Comp> persons;
	cin >> s >> f;
	do {
		do getline(cin, str);
		while (str == "");
		stringstream ss(str);
		if (ss >> ts >> tf) {
			cout << i++ << ". " << minimum(persons) << endl;
			s = ts;
			f = tf;
			for (auto p : persons) delete p;
			persons.clear();
			for (auto p : m) delete p.second;
			m.clear();
		}
		else {
			ss.clear();
			Person *father = nullptr;
			while (ss >> str) {
				auto it = persons.insert(new Person(str));
				if (!father) father = *(it.first);
				else father->kids.insert(*(it.first));
			}
		}
	}
	while (str != "0 0");
}

Out* minimum(set<Person*, Person::Comp> persons)
{
	if (m.count(persons)) return m[persons];
	if (persons.empty()) return m[persons] = new Out();
	Person *p = *persons.begin();
	persons.erase(p);
	Out *c1 = minimum(persons);
	//cout << p->name << "Single: " << s + c1->tcost << endl;
	for (auto ptr : p->kids)
		if (!ptr->kids.size()) persons.erase(ptr);
	Out *c2 = minimum(persons);
	//cout << p->name << "Family: " << f + c2->tcost << endl;
	long scost = s + c1->tcost, fcost = f + c2->tcost;
	return m[persons] = scost < fcost? new Out(scost, c1->tf, 1 + c1->ts) : new Out(fcost, 1 + c2->tf, c2->ts);
}
