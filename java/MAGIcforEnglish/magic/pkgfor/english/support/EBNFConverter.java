/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package magic.pkgfor.english.support;

import java.util.ArrayList;
import java.util.Set;
import magic.pkgfor.english.support.Grammar.Rule;
import magic.pkgfor.english.support.Grammar.Rule.NonTerminal;
import magic.pkgfor.english.support.Grammar.Rule.Symbol;
import magic.pkgfor.english.support.Grammar.RuleSet;

/**
 *
 * @author Saurabh
 */
public class EBNFConverter {
    
    static Grammar G;
    static ProductionDirectory directory;
    
    public static Grammar convert(Grammar gr) throws MalformedGrammarException, TooManyLoopIterationsException   {
        G= gr;
        directory= new ProductionDirectory(gr);
        for(Rule r: G.rules)    {
            if(!r.isChomsky())  throw new IllegalArgumentException("Shit!");
            if(r.symbols.size()== 2)
                terminalise(r);
        }
        removeTerminalProductions();
        removeOnceUsed();
        G.checkCorrectness();
        return G;
    }

    private static void removeOnceUsed() throws TooManyLoopIterationsException {//contains potential exceptions
        RuleSet newRules;
        ArrayList<Symbol> rhs;
        Rule newR;
        int i=0;
        boolean rulesChanged;
        do {
            rulesChanged= false;
            if(i>1000)  throw new TooManyLoopIterationsException();
            newRules= new RuleSet();
            for(Rule r: G.rules)
                if((r.symbols.size()!=1)&&((countOccurence(r.T)!=1)||(r.T.name.equals("S"))))   {
                    newR= new Rule(r.T);
                    for(Symbol s: r.symbols)    {
                        if((s.isNonTerminal())&&(countOccurence(s)==2))    {
                            //to catch an exception later. lhsToRhs.get(r.T) must be a singleton set!
                            rhs= directory.lhsToRhs.get((NonTerminal) s).iterator().next();
                            //indexOf() returns first index. But in this case it must be the only index or something's wrong
                            newR.symbols.addAll(rhs);
                            G.deassign((NonTerminal) s);
                            rulesChanged= true;
                        }
                        else newR.symbols.add(s);
                    }
                    newRules.add(newR);
                }
                else if((r.symbols.size()==1)&&(countOccurence(r.T)!=1))  newRules.add(r);
            if(rulesChanged)    {
                G.rules= newRules;
                directory= new ProductionDirectory(G);
            }
        } while(rulesChanged);
        newRules= new RuleSet();
        for(Rule r: G.rules)
            if((countOccurence(r.T)!=1)||(r.T.name.equals("S")))
                newRules.add(r);
            else G.deassign(r.T);
        G.rules= newRules;
    }

    private static void terminalise(Rule r) {
        ArrayList<Symbol> rhs, newRhs= new ArrayList<>(2);
        Set<ArrayList<Symbol>> rhses;
        for(Symbol s: r.symbols)    {
            rhses= directory.lhsToRhs.get((NonTerminal) s);
            if(rhses==null) { 
                System.err.println("Faulty symbol: "+s.name);
                G.display();
            }
            if(rhses.size()== 1)  {
                rhs= rhses.iterator().next();
                if(rhs.size()== 1)
                   newRhs.add(rhs.get(0));
                else newRhs.add(s);
            }
            else newRhs.add(s);
        }
        r.symbols= newRhs;
    }

    private static void removeTerminalProductions() {
        RuleSet newRules= new RuleSet();
        Set<ArrayList<Symbol>> rhses;
        for(Rule r: G.rules)    {
            rhses= directory.lhsToRhs.get(r.T);
            if((rhses.size()==1)&&(rhses.iterator().next().size()==1))  {
                G.deassign(r.T);
                continue;
            }
            newRules.add(r);
        }
        G.rules= newRules;
        directory= new ProductionDirectory(G);
    }

    private static int countOccurence(Symbol s) {
        int count=0;
        for(Rule r: G.rules)    {
            if(count>2) break;
            if(r.T.name.equals(s.name)) count++;
            for(Symbol c: r.symbols)
                if(c.equals(s)) count++;
        }
        return count;
    }
        
}