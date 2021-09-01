/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package magic.pkgfor.english.support;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import magic.pkgfor.english.support.Grammar.Rule.NonTerminal;
import magic.pkgfor.english.support.Grammar.Rule.Symbol;

/**
 *
 * @author Saurabh
 *
 * This is not a directory of productions in the grammar as such, but rather
 * more of a catalog of those strings that certain left hand sides mapped to
 * at one point. The idea is to avoid, as much as is sensibly possible,
 * redundency in variable assignments.
 */
	class ProductionDirectory {
		/**
		 * Instantiates a production directory.
		 */
		ProductionDirectory(Grammar grammar) {
			// Create the map of LHSes to RHSes.
			for (Grammar.Rule r: grammar.rules) {
				// Check the right hand side map.
				Set<ArrayList<Grammar.Rule.Symbol>> rhses = lhsToRhs.get(r.T);
				if (rhses == null) {
					rhses = new HashSet<>();
					lhsToRhs.put(r.T, rhses);
				}
				rhses.add(r.symbols);
			}
			// Creates the map of RHSes to LHSes.
                        ArrayList <Grammar.Rule.Symbol> rhs;
			Iterator <Map.Entry<Grammar.Rule.NonTerminal, Set<ArrayList<Grammar.Rule.Symbol>>>> it = lhsToRhs.entrySet().iterator();
			while (it.hasNext()) {
				Map.Entry <Grammar.Rule.NonTerminal, Set<ArrayList<Grammar.Rule.Symbol>>> entry = it.next();
				Set<ArrayList<Grammar.Rule.Symbol>> rhses = entry.getValue();
				Iterator <ArrayList<Grammar.Rule.Symbol>> it2 = rhses.iterator();
                                while(it2.hasNext())    {
                                    rhs = it2.next();
                                    rhsToLhs.put(rhs, entry.getKey());
                                }
			}
		}

		/**
		 * After the first initialization, this can be used to add productions.
		 * The left hand side must not have been in any production added before,
		 * or in the initializations.
		 * 
		 * @param production
		 *            the production to add
		 */
		void add(Grammar.Rule r) {
			// Does the RHS already have a unique mapping?
			if (rhsToLhs.containsKey(r.symbols))
				throw new IllegalArgumentException(r.returnRule()
						+ " already represented by " + r.T.name);
			// Add the production.
			Set<ArrayList<Grammar.Rule.Symbol>> rhses = lhsToRhs.get(r.T);
			if (rhses == null) {
				rhses = new HashSet<>();
				lhsToRhs.put(r.T, rhses);
			}
			rhses.add(r.symbols);
			rhsToLhs.put(r.symbols, r.T);
		}

		/** The map of LHS to multiple RHS stored as sets. */
		Map <NonTerminal, Set <ArrayList<Symbol>>>lhsToRhs = new HashMap<>();

		/**
		 * The map of RHS to a LHS, given that the RHS of the production is
		 * unique to the LHS of the production (that is, that LHS maps only to
		 * this RHS).
		 */
		Map <ArrayList<Symbol>, NonTerminal>rhsToLhs = new HashMap<>();
	}
