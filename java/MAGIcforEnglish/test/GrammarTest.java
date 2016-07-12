/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */



import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.NoSuchElementException;
import java.util.StringTokenizer;
import junit.framework.TestCase;
import magic.pkgfor.english.support.Grammar;
import magic.pkgfor.english.support.Grammar.Rule;
import magic.pkgfor.english.support.MalformedGrammarException;
import magic.pkgfor.english.support.TooManyLoopIterationsException;
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

/**
 *
 * @author Saurabh
 */
public class GrammarTest extends TestCase {
    
    private Grammar G;
    
    public GrammarTest() {
    }
    
    @BeforeClass
    public static void setUpClass() {
    }
    
    @AfterClass
    public static void tearDownClass() {
    }
   
    @Before
    @Override
    @SuppressWarnings("null")
    public void setUp() throws FileNotFoundException, IOException {
        String line, token;
        boolean lhs= true;
        StringTokenizer t;
        G= new Grammar();
        Rule r = null;
        BufferedReader b= new BufferedReader(new FileReader(new File("UnitTestCFG.txt")));
        do{
            line= b.readLine();
            if(line!= null) {
                t= new StringTokenizer(line);
                try{
                    while(true) {
                        token= t.nextToken();
                        if(token.startsWith("//"))  break;
                        if(token.equals("-->")) {
                          lhs= false;
                          continue;
                        }
                        if(lhs) r= new Rule(G.assignNonTerminal(token));
                        else    {
                            if(Character.isUpperCase(token.charAt(0)))
                                r.symbols.add(G.assignNonTerminal(token));
                            else r.symbols.add(G.assignTerminal(token));
                        }
                    }
                }catch(NoSuchElementException e){
                    G.rules.add(r);
                }
            }
            lhs= true;
        }
        while(line!=null);
        b.close();
        G.display();
    }
    
    @After
    @Override
    public void tearDown() {
    }

    // TODO add test methods here.
    // The methods must be annotated with annotation @Test. For example:
    //
     @Test
    @SuppressWarnings("null")
    public void testUnitRemoval() throws MalformedGrammarException, TooManyLoopIterationsException {
        Grammar g= null;
        for(int i=1; i<=100; i++)  {
            System.out.println("Pass "+i+".....");
            g= new Grammar(G);
            g.removeNullProductions();
            System.out.println("Succeeded");
        }
        g.display();
    }
    
}

class TestRunner    {
    
        TestCase test= new GrammarTest(){
        @Override
        public void runTest() throws MalformedGrammarException, TooManyLoopIterationsException   {
            testUnitRemoval();
        }
    };
}