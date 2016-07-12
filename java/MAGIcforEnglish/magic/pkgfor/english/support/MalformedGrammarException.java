/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package magic.pkgfor.english.support;

import magic.pkgfor.english.support.Grammar.Rule.NonTerminal;

/**
 *
 * @author Saurabh
 */
public abstract class MalformedGrammarException extends Exception {}

class VariableHasNoRuleException extends MalformedGrammarException  {
    VariableHasNoRuleException(Grammar g)    {
        g.display();
    }
}

class IncorrectNonTerminalSetException extends MalformedGrammarException    {
    IncorrectNonTerminalSetException(Grammar g)  {
        g.display();
    }
}

class MultipleVariablesWithSameNameException extends MalformedGrammarException  {
    MultipleVariablesWithSameNameException(NonTerminal T1, NonTerminal T2)    {
        System.err.println(T1+" & "+T2+ " have same name: "+ T1.name);
    }
}