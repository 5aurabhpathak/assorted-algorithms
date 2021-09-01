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
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import magic.pkgfor.english.support.Grammar.Rule;
import magic.pkgfor.english.support.Grammar.Rule.NonTerminal;

/**
 * CYK Parser 
 * It parses grammar that is in CNF form and returns whether the String is accepted by language or not.
 * 
 * @author Saurabh
 *
 */

public class CYKParser {
		
	/** Map to store the result of subparts */
	private HashMap <String, HashSet<NonTerminal>> myMap;
        
        private final Grammar CNFGrammar;
	
	/**
	 * Constructor for CYK Parser
	 * @param grammar Grammar that is going to be used in CYK Parsing (It will be converted to CNF)
     * @throws magic.pkgfor.english.support.MalformedGrammarException
	 */
        
	public CYKParser(Grammar grammar) throws MalformedGrammarException, TooManyLoopIterationsException
	{
                CNFGrammar= CNFConverter.convert(grammar);
	}
	
        public Grammar getGrammar() {
            return CNFGrammar;
        }
	
	/**
	 * Check whether the grammar accepts the string or not 
	 * using DP
     * @param target
     * @return 
	 */
        public boolean solve(ArrayList <String> target) {
            return solve(target, "Normal");
        }
        
	public boolean solve(ArrayList <String> target, String tableType)
	{
		myMap=new HashMap <>();
                HashSet <NonTerminal> temp;
		int targetLength=target.size();
                boolean success= false;
		for (int i=0; i<targetLength; i++)
		{
			String a=target.get(i);
			temp=new HashSet <>();
			int count=0;

			for (Rule r: CNFGrammar.rules)
			{
				if (r.symbols.get(0).name.equals(a))
				{
					count++;
					temp.add(r.T);
				}
			}
                        if(count!=0)    {
                            String key=i+","+i;
                            myMap.put(key, temp);
                        }
                        else if(!tableType.equals("Detailed")) return false;
		}
		//displayParseTable();
		
		int increment=1;
		for (int i=0; i<targetLength; i++)
		{
			for (int j=0; j<targetLength; j++)
			{
				if (targetLength<=j+increment)
					break;
				int k=j+increment;
				checkProductions(j,k);
				
			//	System.out.print(myMap.get(j+","+k));
			}
			//System.out.println();
			increment++;
		}
		//displayParseTable();
		if (myMap.get("0,"+(targetLength-1))!=null)
                    success= hasStartVariable(myMap.get("0,"+(targetLength-1)));
                return success;
	}
        
        private boolean hasStartVariable(HashSet <NonTerminal> in) {
                for(NonTerminal T: in)
                    if(T.name.equals("S"))
                        return true;
                return false;
        }
	
	/**
	 * Helper method of solve method that checks the surrounding production
	 * @param x
	 * @param y
	 */
	private void checkProductions(int x,int y)
	{
            HashSet <NonTerminal> tempSet=new HashSet <>(), n1, n2;
            for (Rule r: CNFGrammar.rules)
                for (int k=x; k<y; k++)
                {
                    String key1=x+","+k;
                    String key2=(k+1)+","+y;
                    n1= myMap.get(key1);
                    n2= myMap.get(key2);
                    if((n1!= null)&&(n2!=null))
                        for (NonTerminal A : n1)
                                for (NonTerminal B : n2)
                                        if (r.returnRule().equals(A.name+" "+B.name+" "))
                                            tempSet.add(r.T);
                }
            if(!tempSet.isEmpty())
                myMap.put(x+","+y, tempSet);
	}
        
        public HashMap<String, HashSet <NonTerminal>> getParseTable()    {
            return myMap;
        }
        
        public void displayParseTable() {
            for(Map.Entry<String, HashSet<NonTerminal>> entry: myMap.entrySet())  {
                System.out.print(entry.getKey()+"\t");
                for(NonTerminal t: entry.getValue())
                    System.out.print(t.name+"\t");
                System.out.println();
            }
        }
	
}