/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package magic.pkgfor.english.GrammarInference;

import java.util.HashSet;
import magic.pkgfor.english.support.Grammar;
import magic.pkgfor.english.support.Grammar.Rule;
import magic.pkgfor.english.support.Grammar.Rule.NonTerminal;

/**
 *
 * @author Saurabh
 */
public class MutationOperator {
    
    Grammar G;
    public HashSet<Rule> newRules;

    public MutationOperator(Grammar grammar) {
        G= grammar;
        newRules= new HashSet<>();
    }
    
    public void operate(Rule r, int index, String type) {
        switch(type){
            case "option":      option(r, index);          break;
            case "iteration+":  iterationPlus(r, index);   break;
            case "iteration*":  iterationStar(r, index);    break;
        }
    }

    private void option(Rule r, int index) {
        NonTerminal n= G.assignNonTerminal("O"+G.numNT++);
        Rule newR= new Rule(n);
        newR.symbols.add(r.symbols.get(index));
        newRules.add(newR);
        newR= new Rule(n);
        newRules.add(newR);
        r.symbols.set(index, n);
    }

    private void iterationPlus(Rule r, int index) {
        NonTerminal n= G.assignNonTerminal("P"+G.numNT++);
        Rule newR= new Rule(n);
        newR.symbols.add(r.symbols.get(index));
        newR.symbols.add(n);
        newRules.add(newR);
        newR= new Rule(n);
        newR.symbols.add(r.symbols.get(index));
        newRules.add(newR);
        r.symbols.set(index, n);
    }

    private void iterationStar(Rule r, int index) {
        NonTerminal n= G.assignNonTerminal("I"+G.numNT++);
        Rule newR= new Rule(n);
        newR.symbols.add(r.symbols.get(index));
        newR.symbols.add(n);
        newRules.add(newR);
        newR= new Rule(n);
        newRules.add(newR);
        r.symbols.set(index, n);
    }
    
}
