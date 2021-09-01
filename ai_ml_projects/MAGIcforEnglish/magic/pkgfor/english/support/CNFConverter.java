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





package magic.pkgfor.english.support;

import java.util.ArrayList;
import magic.pkgfor.english.support.Grammar.Rule;
import magic.pkgfor.english.support.Grammar.Rule.NonTerminal;
import magic.pkgfor.english.support.Grammar.Rule.Symbol;
import magic.pkgfor.english.support.Grammar.RuleSet;

/**
 * Converts grammars to Chomsky normal form.
 * 
 * @author Saurabh
 */

public class CNFConverter {

	/**
	 * In the {@link #getLeft} function, a new production may be added. After
	 * the function is called, this variable will hold if an addition was made.
	 */
	private static boolean leftAdded;

        public static Grammar convert(Grammar g) throws MalformedGrammarException, TooManyLoopIterationsException    {
            RuleSet cnfRules= new RuleSet();
            System.out.println("Forming CNFGrammar...");
            Timer t= new Timer();
            grammar = new Grammar(g);
            System.out.print("Removing Useless Productions..");
            Timer t1= new Timer();
            grammar.removeUselessProductions();
            System.out.print(t1.getElapsedTime()+" seconds.\nRemoving Null Productions..");
            t1.reset();
            grammar.removeNullProductions();
            System.out.print(t1.getElapsedTime()+" seconds.\nRemoving Unit Productions..");
            if(t1.getElapsedTime()>20.0)
                g.display();
            t1.reset();
            grammar.removeUnitProductions();
            System.out.print(t1.getElapsedTime()+" seconds.\nNow Converting to CNF..");
            t1.reset();
            productionDirectory = new ProductionDirectory(grammar);
            for(Rule r: grammar.rules)
                if(!r.isChomsky())  cnfRules.addAll(replacements(r));
                else    cnfRules.add(r);
            grammar.rules= cnfRules;
            grammar.checkCorrectness();
            System.out.println(t1.getElapsedTime()+" seconds.\nCNF Grammar formed. ("+t.getElapsedTime()+" seconds)");
            return grammar;
        }
        
	/**
	 * Given a symbol string A, even a single symbol, this will return a LHS of
	 * a productions where LHS->A is an okay production to map to A.
	 * 
	 * @param string
	 *            the symbol string
	 * @return a valid left hand side for that string
	 */
	private static NonTerminal getLeft(ArrayList<Symbol> right) {
		NonTerminal left = productionDirectory.rhsToLhs.get(right);
		leftAdded = false;
		if (left != null)
			return left;
		leftAdded = true;
		left = grammar.assignNonTerminal("N"+grammar.numNT++);
		Rule r = new Rule(left);
                r.symbols.addAll(right);
		productionDirectory.add(r);
		return left;
	}

	/**
	 * Returns the array of productions needed to replace a production.
	 * 
	 * @param production
	 *            the production to replace
	 * @return the array of productions that will replace this production
	 * @throws IllegalArgumentException
	 *             if the production does not need to be replaced
	 */
	private static RuleSet replacements(Rule r) {
            ArrayList <Symbol> remainder= new ArrayList<>();
            RuleSet replacement= new RuleSet();
            Rule newR;
            for (Symbol s: r.symbols)
                    if (!s.isNonTerminal())
                        return determinalize(r);
            // No termianls to resolve...
            if (r.symbols.size() <= 2)
                    if (r.symbols.size() == 2)
                            throw new IllegalArgumentException(r
                                            + " has two variables already!");
                    else    {
                        grammar.display();
                            throw new IllegalArgumentException(grammar
                                            + " is in bad form!");
                    }
            // Now we're all right.
            remainder.addAll(r.symbols);
            remainder.remove(0);
            NonTerminal left = getLeft(remainder);
            newR= new Rule(r.T);
            newR.symbols.add(r.symbols.get(0));
            newR.symbols.add(left);
            replacement.add(newR);
            if (leftAdded)  {
                newR= new Rule(left);
                newR.symbols.addAll(remainder);
                if(!newR.isChomsky())
                    replacement.addAll(replacements(newR));
                else replacement.add(newR);
            }
            return replacement;
	}

	/**
	 * De-terminalizes a production.
	 * 
	 * @param production
	 *            a production to "determinalize"
	 * @return the determinalized production
	 */
	private static RuleSet determinalize(Rule r) {
		RuleSet list= new RuleSet();
		ArrayList <Symbol> rhs= new ArrayList<>();
                Rule newRule;
		for (Symbol s: r.symbols) {
			if (!s.isNonTerminal()) {
                                ArrayList <Symbol> temp= new ArrayList<>();
                                temp.add(s);
				NonTerminal newNT = getLeft(temp);
				if (leftAdded)  {
                                    newRule= new Rule(newNT);
                                    newRule.symbols.add(s);
                                    list.add(newRule);
                                }
				rhs.add(newNT);
			} else
				rhs.add(s);
		}
                newRule= new Rule(r.T);
                newRule.symbols.addAll(rhs);
                if(!newRule.isChomsky())
                    list.addAll(replacements(newRule));
                else list.add(newRule);
		return list;
	}

	/** The production directory. */
	private static ProductionDirectory productionDirectory;

	/** The grammar we're converting. */
	private static Grammar grammar;
     
}