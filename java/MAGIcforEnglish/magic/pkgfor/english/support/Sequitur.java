package magic.pkgfor.english.support;

import java.util.ArrayList;
import magic.pkgfor.english.support.Grammar.Rule;
import magic.pkgfor.english.support.Grammar.Rule.NonTerminal;
import magic.pkgfor.english.support.Grammar.Rule.Symbol;
import magic.pkgfor.english.support.Grammar.Rule.Terminal;

public final class Sequitur
{

    private static final class Digram
    {
	Symbol [] s= new Symbol[2];
	void append(Symbol t1, Symbol t2)
	{
		this.s[0]= t1;
		this.s[1]=t2;
	}
        boolean isRule(Rule r) {
            if((r.symbols.size()==2)&&((r.symbols.get(0).name.equals(this.s[0].name))&&(r.symbols.get(1).name.equals(this.s[1].name))))
                return true;
            return false;
        }
    }

    private static final ArrayList <Digram> digrams= new ArrayList<>();
    private static Rule S;
    private static Grammar G;

    public static Grammar sequiturAlgo(ArrayList <String> tags)
    {
    	Terminal t;
    	Digram d;
	int i=0;
        G= new Grammar();
        S= new Rule(G.assignNonTerminal("S"));
        G.rules.add(S);
        while(i<tags.size())
	{
            t= G.assignTerminal(tags.get(i));
            S.symbols.add(t);
            if(i++>0)
            {
                    d= new Digram();
                    d.append(S.symbols.get(S.symbols.size()-2), t);
                    digrams.add(d);
                    enforceUniqueness(d);
            }
	}
        //G.display();
        return G;
    }
	private static void enforceUniqueness(Digram d)
	{
		NonTerminal NT;
		Rule S1;
		int index= match(d);
                if(index!=-1)
		{
			NT= G.assignNonTerminal("N"+G.numNT++);
			S1= new Rule(NT);
			replace(d, NT);
			S1.symbols.add(d.s[0]);
			S1.symbols.add(d.s[1]);
			add(S1, d);
                        digrams.clear();
			refillDigram();
                        removeOnceUsed();
                        for (int i=0; i<digrams.size(); i++)
                        enforceUniqueness(digrams.get(i));
		}
	}

        private static int match(Digram d)
	{
		Digram d1;
		for(int i=0; i<digrams.size(); i++)
		{
			d1= digrams.get(i);
                        if((!d1.equals(d))&&((d.s[0].name.equals(d1.s[0].name))&&(d.s[1].name.equals(d1.s[1].name))))
				return i;
		}
		return -1;
	}

    private static void removeOnceUsed() {    
        for(Digram dig : digrams)   {
            if(dig.s[0].isNonTerminal())
                checkOnceAndEnforce(dig.s[0]);
            else if(dig.s[1].isNonTerminal())
                checkOnceAndEnforce(dig.s[1]);
        }
    }

    private static void checkOnceAndEnforce(Symbol symb) {
        int count = 0;
        Rule toBeModified= null;
        for(Rule r: G.rules)  {
            for(Symbol s: r.symbols)
                if(s.name.equals(symb.name))    {
                    count++;
                    if(count==1)
                        toBeModified= r;
                    else if(count>1) break;
                }
            if(count>1) break;
        }
        if(count== 1)
            enforceOnce(symb, toBeModified, toBeModified.symbols.indexOf(symb));
    }

    private static void enforceOnce(Symbol symb, Rule modify, int index) {
        Rule deleted= null;
        for(Rule r: G.rules)
            if(r.T.equals(symb))    {
                deleted= r;
                G.deassign(r.T);
                G.rules.remove(r);
                break;
            }
        modify.replace(index, deleted.symbols); 
    }

    private static void refillDigram() {
        Digram dig;
        int i=0;
        for(Rule r: G.rules)  {
            for(Symbol sym: r.symbols)  {
                if(i>0)   {
                dig= new Digram();
		dig.append(r.symbols.get(i-1), sym);
                digrams.add(dig);
                }
            i++;
            }
            i=0;
        }
    }
    
    private static void replace(Digram dig, NonTerminal NT)
    {   
        NonTerminal replacement= NT;
        for(Rule r: G.rules)
            if(dig.isRule(r))
                replacement= r.T;
        for(Rule r: G.rules )
            for(int i=1; i<r.symbols.size(); i++)
                if((!dig.isRule(r))&&(dig.s[0].name.equals(r.symbols.get(i-1).name))&&(dig.s[1].name.equals(r.symbols.get(i).name)))  {
                    r.symbols.remove(i);
                    r.symbols.remove(i-1);
                    r.symbols.add(i-1, replacement);
                }
    }

    private static void add(Rule S1,Digram dig) {
        boolean alreadyHas= false;
        for(Rule r: G.rules)
            if(dig.isRule(r))    {
                    alreadyHas= true;
                    G.deassign(S1.T);
                    break;
            }
        if(!alreadyHas)
            G.rules.add(S1);
    }
}