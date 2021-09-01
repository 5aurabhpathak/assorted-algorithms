/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package magic.pkgfor.english.GrammarInference;

import java.util.ArrayList;
import java.util.HashSet;
import magic.pkgfor.english.support.Grammar;
import magic.pkgfor.english.support.Grammar.Rule;
import magic.pkgfor.english.support.Grammar.Rule.NonTerminal;
import magic.pkgfor.english.support.Grammar.Rule.Symbol;
import magic.pkgfor.english.support.MalformedGrammarException;
import magic.pkgfor.english.support.TooManyLoopIterationsException;

/**
 *
 * @author Saurabh
 */
class Generalizer {
    
    static Grammar g1, g2;

    static void generalize(Grammar ebnfg) throws TooManyLoopIterationsException, MalformedGrammarException {
        step1(ebnfg);
    }

    private static void step1(Grammar ebnfg) throws TooManyLoopIterationsException, MalformedGrammarException {//what about nested structures of size>2?
        Rule n;
        Symbol first, second, last, secondLast;
        NonTerminal nt;
        HashSet<Rule> addition= new HashSet<>();
        for(Rule r: ebnfg.rules)
            if(r.symbols.size()>4)    {
                first= r.symbols.get(0);
                second= r.symbols.get(1);
                last= r.symbols.get(r.symbols.size()-1);
                secondLast= r.symbols.get(r.symbols.size()-2);
                if((first.equals(second))&&(last.equals(secondLast)))  {
                    nt= ebnfg.assignNonTerminal("G"+ebnfg.numNT++);
                    n= new Rule(nt);
                    n.symbols.addAll(r.symbols.subList(2, r.symbols.size()-3));
                    r.symbols= new ArrayList<>();
                    r.symbols.add(first);
                    r.symbols.add(second);
                    r.symbols.add(nt);
                    r.symbols.add(last);
                    r.symbols.add(secondLast);
                    addition.add(n);
                }
            }
        g1= new Grammar(ebnfg);
        g1.rules.addAll(addition);
        step2(g1);
    }

    private static void step2(Grammar g) throws TooManyLoopIterationsException, MalformedGrammarException {
        for(Rule r1: g.rules)
            if(!r1.symbols.isEmpty())
                for(Rule r2: g.rules)
                    if((!r2.equals(r1))&&(!r1.isRecursive()))
                        r2.replace(r1.symbols, r1.T);
        step3(g);
    }

    private static void step3(Grammar g) throws TooManyLoopIterationsException, MalformedGrammarException {
        ArrayList<Symbol> temp;
        Symbol stemp;
        HashSet<Rule> addition= new HashSet<>(), addition2= new HashSet<>();
        int i;
        for(Rule rule: g.rules) {
            if(rule.symbols.size()<3)  continue;
            stemp= rule.symbols.get(0);
            temp= new ArrayList<>();
            temp.add(stemp);
            for(i=1; i<rule.symbols.size(); i++)    {
                if(rule.symbols.get(i).equals(stemp))   {
                    temp.add(stemp);
                    continue;
                }
                else if(temp.size()!=1) {
                    iterate(g, rule, addition, addition2, stemp, temp);
                    i= i-temp.size()+1;
                }
                temp= new ArrayList<>();
                stemp= rule.symbols.get(i);
                temp.add(stemp);
            }
            //potential bug in condition
            if(temp.size()!=1)
                iterate(g, rule, addition, addition2, stemp, temp);
        }
        g2= new Grammar(g);
        g.rules.addAll(addition);
        g.removeUnitProductions();
        g.checkCorrectness();
        g2.rules.addAll(addition2);
        g2.removeUnitProductions();
        g2.checkCorrectness();
    }
    
    private static void iterate(Grammar ebnfg, Rule rule, HashSet<Rule> addition, HashSet<Rule> addition2, Symbol stemp, ArrayList<Symbol> temp) throws TooManyLoopIterationsException  {
        NonTerminal n= ebnfg.assignNonTerminal("G"+ebnfg.numNT++);
        Rule r= new Rule(n);
        r.symbols.add(stemp);
        r.symbols.add(n);
        addition.add(r);
        addition2.add(new Rule(r));
        r= new Rule(n);
        r.symbols.add(stemp);
        addition.add(r);
        r= new Rule(n);
        addition2.add(r);
        rule.replace(temp, n);
    }
    
}
