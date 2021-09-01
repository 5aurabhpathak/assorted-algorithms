/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package magic.pkgfor.english.GrammarInference;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Random;
import java.util.TreeMap;
import magic.pkgfor.english.support.CNFConverter;
import magic.pkgfor.english.support.CYKParser;
import magic.pkgfor.english.support.EBNFConverter;
import magic.pkgfor.english.support.Grammar;
import magic.pkgfor.english.support.Grammar.Rule;
import magic.pkgfor.english.support.MalformedGrammarException;
import magic.pkgfor.english.support.POSTagger;
import magic.pkgfor.english.support.Sequitur;
import magic.pkgfor.english.support.Timer;
import magic.pkgfor.english.support.TooManyLoopIterationsException;

/**
 *
 * @author Saurabh
 */
public final class MAGIcComponents {

    public MAGIcComponents(int pS, double pM) {
        popSize= pS;
        Pm= pM;
        population= new ArrayList<>(pS);
        sentences= new ArrayList<>();
        sentence= new ArrayList<>();
    }

    private int popSize;
    public final ArrayList <Grammar> population;
    private final ArrayList <Grammar> popSizePlusDelta= new ArrayList<>(popSize);
    private final ArrayList <ArrayList <String>> sentences;
    private ArrayList <String> sentence;
    private final double Pm;
    
    public void initialize() throws MalformedGrammarException, TooManyLoopIterationsException {
        for(String tag: POSTagger.tags) {
            sentence.add(tag);
            if(tag.equals("."))    {
                sentences.add(sentence);
                sentence= new ArrayList<>();
            }
        }
        System.out.println("Sample size is "+sentences.size()+". Now Processing...");
        for(ArrayList <String> s: sentences)
        {
            Grammar g= Sequitur.sequiturAlgo(s);
            population.add(g);
            g.fitness= fitnessOf(g);
        }
    }

    public void improveAndEvaluate() throws MalformedGrammarException, TooManyLoopIterationsException {
        Grammar newG= null;
        for(Grammar g: population)  {
            if(g.falseNegative!=null)  {
                newG= g.parser.getGrammar();
                g.parser.solve(g.falseNegative, "Detailed");
                addRule(newG, g.parser.getParseTable(), g.falseNegative);
                newG= CNFConverter.convert(newG);
            }
            if(newG!= null) {
                newG.fitness= fitnessOf(newG);
                if(newG.fitness>0)  popSizePlusDelta.add(EBNFConverter.convert(newG));
            }
            popSizePlusDelta.add(g);
        }
    }
    
    private double fitnessOf(Grammar grammar) throws MalformedGrammarException, TooManyLoopIterationsException  {
        double posSample=0;
        Timer t;
        grammar.parser= new CYKParser(grammar);
        grammar.falseNegative= null;
        t= new Timer();
        for(ArrayList <String> s: sentences)
            if(grammar.parser.solve(s))
                posSample++;
            else grammar.falseNegative= s;
        System.out.println("Parsing took "+t.getElapsedTime()+" seconds.");
        return posSample-grammar.size()*0.0005;
    }
    
    public void mutate() throws MalformedGrammarException, TooManyLoopIterationsException {
        Random rnd= new Random();
        MutationOperator m;
        int i;
        for (Iterator<Grammar> it = popSizePlusDelta.iterator(); it.hasNext();) {
            Grammar g = it.next();
            m= new MutationOperator(g);
            for(Rule rule: g.rules)
                for(i=0; i<rule.symbols.size(); i++)    {
                    if(Math.random()<=Pm)    {
                        switch(rnd.nextInt(3))    {
                            case 0: m.operate(rule, i, "option");       break;
                            case 1: m.operate(rule, i, "iteration+");   break;
                            case 2: m.operate(rule, i, "iteration*");
                        }
                    }
                }
            if(g.rules.addAll(m.newRules))  {
                g.fitness= fitnessOf(g);
                if(g.fitness==0) it.remove();
            }
        }
    }

    public void generalize() throws TooManyLoopIterationsException, MalformedGrammarException {
        ArrayList<Grammar> temp= new ArrayList<>(popSizePlusDelta.size()*2);
        for(Grammar g: popSizePlusDelta)  {
            Generalizer.generalize(g);
            Generalizer.g1.fitness= fitnessOf(Generalizer.g1);
            Generalizer.g2.fitness= fitnessOf(Generalizer.g2);
            if(Generalizer.g1.fitness>0)    temp.add(Generalizer.g1);
            if(Generalizer.g2.fitness>0)    temp.add(Generalizer.g2);
        }
        popSizePlusDelta.addAll(temp);
    }
    
    public void select() throws MalformedGrammarException   {
        population.clear();
        checkAndRemoveDuplicateGrammars();
        if(popSizePlusDelta.size()>popSize) {
            Collections.sort(popSizePlusDelta, new FitestGrammars());
            population.addAll(popSizePlusDelta.subList(0, popSize));
        }
        else population.addAll(popSizePlusDelta);
        popSizePlusDelta.clear();
        for(Grammar g: population)
            g.checkCorrectness();
    }

    private void addRule(Grammar g, HashMap<String, HashSet<Rule.NonTerminal>> parseTable, ArrayList<String> sneg) {
        Rule r = new Rule(g.assignNonTerminal("S"));
        TreeMap<Integer, Integer> positions = new TreeMap<>();
        int index, j = -1;
        for (String s : parseTable.keySet()) {
            index = s.indexOf(",");
            Integer key = Integer.parseInt(s.substring(0, index));
            Integer value = Integer.parseInt(s.substring(index + 1));
            if ((positions.containsKey(key)) && (value <= positions.get(key))) {
                continue;
            }
            positions.put(key, value);
        }
        for (Integer i : positions.keySet()) {
            if ((positions.get(i) <= j) || (i <= j)) {
                continue;
            }
            while (j + 1 < i) {
                r.symbols.add(g.assignTerminal(sneg.get(j++ + 1)));
            }
            r.symbols.add(parseTable.get(i + "," + positions.get(i)).iterator().next());
            j = positions.get(i);
        }
        g.rules.add(r);
    }

    private void checkAndRemoveDuplicateGrammars() {
        int i, j;
        ArrayList <Grammar> duplicates= new ArrayList<>();
        for(i=0; i< popSizePlusDelta.size()-1; i++)
            for(j=i+1; j<popSizePlusDelta.size(); j++)
                if(popSizePlusDelta.get(i).isSameAs(popSizePlusDelta.get(j)))   {
                    duplicates.add(popSizePlusDelta.get(i));
                    break;
                }
        for(Grammar g: duplicates)
            popSizePlusDelta.remove(g);
    }
    
    private static final class FitestGrammars implements Comparator <Grammar>  {

        @Override
        public int compare(Grammar g1, Grammar g2) {
            if(g1.fitness>g2.fitness)
                return -1;
            if(g1.fitness<g2.fitness)
                return 1;
            return 0;
        }
        
    }
}