/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package magic.pkgfor.english.support;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Stack;
import java.util.logging.Level;
import java.util.logging.Logger;
import magic.pkgfor.english.support.Grammar.Rule;
import magic.pkgfor.english.support.Grammar.Rule.NonTerminal;
import magic.pkgfor.english.support.Grammar.Rule.Symbol;
import magic.pkgfor.english.support.Grammar.Rule.Terminal;

/**
 *
 * @author Saurabh
 */
public final class Grammar {
    
    public Grammar()    {
        rules= new RuleSet();
        nonTerminalSet= new HashSet<>();
        terminalSet= new HashSet<>();
    }
    
    public Grammar(Grammar old) {
        rules= new RuleSet(old.rules.size());
        for(Rule r: old.rules)
            rules.add(new Rule(r));
        nonTerminalSet= new HashSet<>(old.nonTerminalSet.size());
        nonTerminalSet.addAll(old.nonTerminalSet);
        terminalSet= new HashSet<>(old.terminalSet.size());
        terminalSet.addAll(old.terminalSet);
        numNT= old.numNT;
    }
    
    public void removeUnitProductions() throws MalformedGrammarException, TooManyLoopIterationsException {
        HashMap <NonTerminal, HashSet<NonTerminal>> unitPairs= new HashMap<>();
        HashSet <NonTerminal> mappings;
        Rule R;
        boolean changed;
        int i=0;
        for (Iterator<Rule> it = rules.iterator(); it.hasNext();) {
            Rule r = it.next();
            if((r.symbols.size()==1)&&(r.symbols.get(0).isNonTerminal()))   {
                if(r.T.equals(r.symbols.get(0)))    {
                    it.remove();
                    continue;
                }
                else if(unitPairs.containsKey(r.T)) unitPairs.get(r.T).add((NonTerminal)r.symbols.get(0));
                else    {
                    mappings= new HashSet<>();
                    mappings.add((NonTerminal)r.symbols.get(0));
                    unitPairs.put(r.T, mappings);
                }
                it.remove();
            }
        }
        do{
            changed= false;
            if(i++>1000)    throw new TooManyLoopIterationsException();
            for(NonTerminal T: unitPairs.keySet())  {
                mappings= new HashSet<>();
                for(NonTerminal F: unitPairs.get(T))
                    if(unitPairs.containsKey(F))
                        for(NonTerminal E: unitPairs.get(F))
                            if(!E.equals(T))    mappings.add(E);
                if(unitPairs.get(T).addAll(mappings))   changed= true;
            }
        }   while(changed);
        for(NonTerminal T: unitPairs.keySet())
            for(NonTerminal F: unitPairs.get(T))
                for(Rule r: rulesOf(F)) {
                    R= new Rule(r);
                    R.T= T;
                    rules.add(R);
                }
        checkCorrectness();
    }
    
    public void removeNullProductions() throws MalformedGrammarException, TooManyLoopIterationsException {
        HashSet<NonTerminal> nullable = new HashSet<>(nonTerminalSet.size());
        Terminal dummy= new Terminal("dummy");
        for (Iterator<Rule> it = rules.iterator(); it.hasNext();) {
            Rule r = it.next();
            if(r.symbols.isEmpty()) {
                nullable.add(r.T);
                it.remove();
            }
        }
        if(nullable.isEmpty())  return;
        for(NonTerminal t: nonTerminalSet)
            try{
                isNullable(new Stack<>(), t, nullable);
            }   catch(StackOverflowError e)    {
                System.out.println("Cant' determine whether nullable: "+t.name+"\nNullable Symbols:");
                for(NonTerminal T: nullable)
                    System.out.println(T.name);
                display();
                System.exit(-3);
            }
        for(NonTerminal t: nullable)
            for(Rule r: findUsages(t))
                try{
                    rules.addAll(alternatives(r, t, dummy));
                }   catch(StackOverflowError e)    {
                    System.out.println("Cant find alternatives: "+r.T.name+" --> "+r.returnRule());
                    display();
                    System.exit(-7);
                }
              
        removeNonGenerating();
        checkCorrectness();
    }
    
    private boolean isNullable(Stack <NonTerminal> callers, NonTerminal t, HashSet <NonTerminal> nullable)   {
        boolean nullableSymbol= true;
        if(nullable.contains(t))    return true;
        callers.push(t);
        for(Rule r: rulesOf(t)) {
            nullableSymbol= true;
            for(Symbol s: r.symbols)
                if((!s.isNonTerminal())||(callers.contains((NonTerminal)s))||(!isNullable(callers, (NonTerminal)s, nullable))) {
                    nullableSymbol= false;
                    break;
                }
            if(nullableSymbol)  {
                nullable.add(t);
                callers.pop();
                return true;
            }
        }
        callers.pop();
        return nullableSymbol;
    }
    
    private RuleSet alternatives(Rule r, NonTerminal s, Terminal dummy) throws TooManyLoopIterationsException    {
        RuleSet addition= new RuleSet();
        Rule r1= new Rule(r), r2;
        if(!r1.symbols.remove(s))  return addition;
        if(!r1.symbols.isEmpty())   {                
            addition.addAll(alternatives(r1, s, dummy));
            r2= new Rule(r1);
            r2.replace(dummy, s);
            addition.add(r2);
        }
        r2= new Rule(r);
        r2.symbols.set(r2.symbols.indexOf(s), dummy);
        addition.addAll(alternatives(r2, s, dummy));
        r2.replace(dummy, s);
        addition.add(r2);
        return addition;
    }
      
    private RuleSet findAllOccurences(Symbol T) {
        RuleSet occured= new RuleSet();
        for(Rule r: rules)  {
            if(r.T.equals(T))   {
                occured.add(r);
                continue;
            }
            for(Symbol s: r.symbols)
                if(s.equals(T)) {
                    occured.add(r);
                    break;
                }
        }
        return occured;
    }
    
    private RuleSet findUsages(NonTerminal T)   {
        RuleSet occured= new RuleSet();
        for(Rule r: rules)
            for(Symbol s: r.symbols)
                if(s.equals(T)) {
                    occured.add(r);
                    break;
                }
        return occured;
    }
    
    private RuleSet rulesOf(NonTerminal T)   {
        RuleSet occured= new RuleSet();
        for(Rule r: rules)
            if(r.T.equals(T))
                occured.add(r);
        return occured;
    }
    
    public void removeUselessProductions() throws MalformedGrammarException, TooManyLoopIterationsException  {
        removeNonGenerating();
        removeNonReachable();
        checkCorrectness();
    }
    
    private void removeNonReachable() throws TooManyLoopIterationsException {
        HashSet <NonTerminal> reachableSet= new HashSet<>(nonTerminalSet.size()), temp;
        boolean changed;
        int i=0;
        for(NonTerminal t: nonTerminalSet)
            if(t.name.equals("S"))  {
                reachableSet.add(t);
                break;
            }
        do  {
            if(i++>1000)    throw new TooManyLoopIterationsException();
            temp= new HashSet<>();
            for(NonTerminal t: reachableSet)
                for(Rule r: rulesOf(t))
                    for(Symbol s: r.symbols)
                        if(s.isNonTerminal()) temp.add((NonTerminal)s);
            changed= reachableSet.addAll(temp);
        } while(changed);
        for(NonTerminal t: nonTerminalSet)
            if(!reachableSet.contains(t))
                for (Iterator<Rule> it = rules.iterator(); it.hasNext();) {
                    Rule r = it.next();
                    if(r.T.equals(t))
                        it.remove();
                }                      
        nonTerminalSet= reachableSet;
    }
    
    @SuppressWarnings("CallToPrintStackTrace")
    private void removeNonGenerating()  {
        HashSet <NonTerminal> generatingSet= new HashSet<>(nonTerminalSet.size());
        boolean allTerminals;
        for(Rule r: rules)  {
            if(generatingSet.contains(r.T)) continue;
            allTerminals= true;
            for(Symbol s: r.symbols)
                if(s.isNonTerminal())   {
                    allTerminals= false;
                    break;
                }
            if(allTerminals) generatingSet.add(r.T);
        }
        for(NonTerminal t: nonTerminalSet)
            try{
                isGenerating(new Stack<>(), t, generatingSet);
            }   catch(StackOverflowError e) {
                System.out.println("Cant determine whether generating: "+t.name+""
                        + "Generating Set:");
                for(NonTerminal T: generatingSet)
                    System.out.println(T.name);
                display();
                e.printStackTrace();
                System.exit(-5);
            }
        for(NonTerminal t: nonTerminalSet)
            if(!generatingSet.contains(t)) 
                for(Rule r: findAllOccurences(t))
                    rules.remove(r);
        nonTerminalSet= generatingSet;
    }
        
    public Terminal assignTerminal(String get) {
        Terminal newT;
        for (Terminal tm : terminalSet)
            if (tm.name.equals(get))
                return tm;
        newT = new Terminal(get);
        terminalSet.add(newT);
        return newT;
    }

    public NonTerminal assignNonTerminal(String get) {
        NonTerminal newNT;
        for (NonTerminal ntm : nonTerminalSet)
            if (ntm.name.equals(get))
                return ntm;
        newNT = new NonTerminal(get);
        nonTerminalSet.add(newNT);
        return newNT;
    }

    void deassign(NonTerminal T) {
        nonTerminalSet.remove(T);
    }

    private boolean isGenerating(Stack <NonTerminal> callers, NonTerminal T, HashSet <NonTerminal> gS) {
        boolean generating= false;
        if(gS.contains(T))  return true;
        callers.push(T);
        for(Rule r: rulesOf(T)) {
                generating= true;
                for(Symbol s: r.symbols)
                    if((s.isNonTerminal())&&((callers.contains((NonTerminal)s))||(!isGenerating(callers, (NonTerminal)s, gS)))) {
                        generating= false;
                        break;
                    }
                if(generating)  {
                    gS.add(T);
                    callers.pop();
                    return true;
                }
        }
        callers.pop();
        return generating;
    }

    public void checkCorrectness() throws MalformedGrammarException {
        ProductionDirectory p= new ProductionDirectory(this);
        HashSet<NonTerminal> nts= new HashSet<>();
        for(Rule r: rules)  {
            nts.add(r.T);
            for(Symbol s: r.symbols)
                if(s.isNonTerminal())   nts.add((NonTerminal)s);
        }
        for(NonTerminal t: nts)
            if(!p.lhsToRhs.containsKey(t))  {
                System.err.println(t.name+ "has no mapping in following grammar!");
                throw new VariableHasNoRuleException(this);
            }
        if(!((nonTerminalSet.containsAll(nts))&&(nts.containsAll(nonTerminalSet)))) {
            System.err.println("NonTerminal set has a problem! Either some Symbols are "
                    + "extra or missing in the following grammar!");
            throw new IncorrectNonTerminalSetException(this);
        }
    }
    
    public int size()   {
        int s= 0;
        for(Rule r: rules)
            s+= r.symbols.size()+1;
        return s;
    }

    //based on heuristical approaches. This method does not guarantee accuracy
    //However, it gets very close to accurately differentiating grammars without
    //using complex logic.
    public boolean isSameAs(Grammar get) {
        boolean atLeastOne;
        if((size()!=get.size())||(rules.size()!=get.rules.size()))  return false;
        else if(nonTerminalSet.size()!= get.nonTerminalSet.size())  return false;
        else if(fitness!= get.fitness)    return false;
        for(Rule r1: rules) {
            atLeastOne= false;
            for(Rule r2: rules)
                if(r2.symbols.size()==r1.symbols.size())    {
                    atLeastOne= true;
                    break;
                }
            if(!atLeastOne) return false;
        }
        return true;
    }
       
    public static final class Rule {
        
        public Rule(Rule old)   {
            T= old.T;
            symbols.addAll(old.symbols);
        }
        
        public boolean isRecursive() {
            for(Symbol s: symbols)
                if(s.equals(T))
                    return true;
            return false;
        }

	public boolean isChomsky() {
		switch (symbols.size()) {
		case 1:
			return !(symbols.get(0).isNonTerminal());
		case 2:
			return symbols.get(0).isNonTerminal() && symbols.get(1).isNonTerminal();
		default:
			return false;
		}
	}

        abstract public static class Symbol {

            public String name;
            public abstract boolean isNonTerminal();
            
        }

        public static final class NonTerminal extends Symbol {

            private NonTerminal(String t) {
                this.name = t;
            }
            
            @Override
            public boolean isNonTerminal() {
                return true;
            }
        }

        public static final class Terminal extends Symbol {

            private Terminal(String c) {
                this.name = c;
            }
            
            @Override
            public boolean isNonTerminal()  {
                return false;
            }
        }
        
        public NonTerminal T;
        public ArrayList<Symbol> symbols = new ArrayList<>();

        public Rule(NonTerminal N) {
            this.T = N;
        }

        public String returnRule() {
            String rule = "";
            if(symbols.isEmpty())  return "\u03F5";
            for (Symbol s : this.symbols) {
                rule = rule.concat(s.name + " ");
            }
            return rule;
        }

        public void replace(int index, ArrayList<Symbol> symbs) {
            this.symbols.remove(index);
            this.symbols.addAll(index, symbs);
        }
        
        public boolean replace(ArrayList<Symbol> symbs, Symbol nt) throws TooManyLoopIterationsException    {
            int i, j, k=0;
            boolean success= false;
            while(Collections.indexOfSubList(symbols, symbs)!=-1)   {
                if(++k>100) throw new TooManyLoopIterationsException();
                i= Collections.indexOfSubList(symbols, symbs);
                for(j=0; j<symbs.size(); j++)
                    symbols.remove(i);
                symbols.add(i, nt);
                success= true;
            }
            return success;
        }
        
        public boolean replace(Symbol s1, Symbol s2)   {
            return Collections.replaceAll(symbols, s1, s2);
        }

    }
    
    private HashSet<Terminal> terminalSet;
    private HashSet<NonTerminal> nonTerminalSet;
    public RuleSet rules;
    public CYKParser parser;
    public ArrayList<String> falseNegative;
    public int numNT;
    public double fitness;

    public void display() {
        ArrayList<Rule> ruleList = new ArrayList<>();
//        ArrayList<NonTerminal> symbolList= new ArrayList<>();
//        symbolList.addAll(nonTerminalSet);
//        Collections.sort(symbolList, new NonTerminalOrder());
        ruleList.addAll(rules);
        Collections.sort(ruleList, new RuleOrder());
        System.out.println("Length: "+rules.size());
        for (Rule r : ruleList)
            System.out.println(r.T.name + " -->  " + r.returnRule());
//        System.out.println("Non Terminals:");
//        for(Symbol T: symbolList)
//            System.out.println(T.name);
    }
    
    public static final class RuleSet extends HashSet <Rule>  {
              
        public RuleSet(int size)    {
            super(size);
        }
        
        public RuleSet()    {
            super();
        }
        
        @Override
        @SuppressWarnings("empty-statement")
        public boolean add(Rule r) {
            String ruleString= r.T.name+" --> "+r.returnRule();
            for(Rule rule: this)
                if((rule.T.name+" --> "+rule.returnRule()).equals(ruleString))
                    return false;
            return super.add(r);
        }
        
        @Override
        public boolean addAll(Collection c)    {
            int oldSize= size();
            for(Object r: c)
                add((Rule)r);
            if(oldSize<size())
                return true;
            return false;
        }
    }

    private static final class RuleOrder implements Comparator<Rule> {

        @Override
        public int compare(Rule o1, Rule o2) {
            return new NonTerminalOrder().compare(o1.T, o2.T);
        }
        
    }
    
    private static final class NonTerminalOrder implements Comparator<NonTerminal>    {

        @Override
        public int compare(NonTerminal o1, NonTerminal o2) {
            if (o1.name.equals(o2.name)) {
                if(o1.equals(o2))   return 0;
                else try {
                    throw new MultipleVariablesWithSameNameException(o1, o2);
                } catch (MultipleVariablesWithSameNameException ex) {
                    Logger.getLogger(Grammar.class.getName()).log(Level.SEVERE, null, ex);
                }
            }
            if (o1.name.equals("S")) {
                return -1;
            }
            if (o2.name.equals("S")) {
                return 1;
            }
            int o1int = Integer.parseInt(o1.name.substring(1));
            int o2int = Integer.parseInt(o2.name.substring(1));
            if (o1int > o2int) {
                return -1;
            }
            return 1;
        }
        
    }
}