/*
 *  JFLAP - Formal Languages and Automata Package
 * 
 * 
 *  Susan H. Rodger
 *  Computer Science Department
 *  Duke University
 *  August 27, 2009

 *  Copyright (c) 2002-2009
 *  All rights reserved.

 *  JFLAP is open source software. Please see the LICENSE for terms.
 *
 */






import java.util.ArrayList;
import magic.pkgfor.english.support.Grammar;
import magic.pkgfor.english.support.Grammar.Rule;
import magic.pkgfor.english.support.Grammar.Rule.NonTerminal;
import magic.pkgfor.english.support.Grammar.Rule.Terminal;

/**
 * CYK Parser tester.
 * @author Kyung Min (Jason) Lee
 *
 */
public class CYKTester {

	public static void main(String[] args)
	{
		Grammar g=new Grammar();
                NonTerminal S= g.assignNonTerminal("S");
                Terminal a= g.assignTerminal("a");
                Terminal b= g.assignTerminal("b");
                Terminal c= g.assignTerminal("c");
                Terminal n= g.assignTerminal("n");
		Rule rule= new Rule(S);
                rule.symbols.add(a);
                rule.symbols.add(b);
                rule.symbols.add(c);
                rule.symbols.add(b);
                rule.symbols.add(a);
                rule.symbols.add(b);
                g.rules.add(rule);
		rule= new Rule(S);
                rule.symbols.add(b);
                rule.symbols.add(b);
                rule.symbols.add(n);
                rule.symbols.add(b);
                rule.symbols.add(a);
                rule.symbols.add(b);
                g.rules.add(rule);
		ArrayList <String> target= new ArrayList<>();
                target.add("a");
                target.add("b");
                target.add("a");
                target.add("b");
                target.add("b");
//		CYKParser parser=new CYKParser(g);
                g.display();
                System.out.println(g.rules.toString());
                Grammar g1= new Grammar(g);
                rule.symbols.remove(n);
                System.out.println(g1.rules.toString());
                g.display();
                g1.display();
//		System.out.println(parser.solve(target));
		//System.out.println("Trace = \n");
                //for(Rule r: parser.getTrace())
                  //  System.out.print(r.T.name+" --> "+r.returnRule()+"\t");
//                parser.displayParseTable();
	}
}
