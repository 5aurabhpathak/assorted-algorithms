/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package magic.pkgfor.english;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import javax.swing.SwingWorker;
import magic.pkgfor.english.GrammarInference.MAGIcComponents;
import magic.pkgfor.english.support.Grammar;
import magic.pkgfor.english.support.Grammar.Rule;
import magic.pkgfor.english.support.MalformedGrammarException;
import magic.pkgfor.english.support.POSTagger;
import magic.pkgfor.english.support.Timer;
import magic.pkgfor.english.support.TooManyLoopIterationsException;

/**
 *
 * @author Saurabh
 */
public final class MAGIcForEnglish extends SwingWorker<Void, Void>  {
    
    private final File f;
    private final double Pm;
    private final int numGen, popSize;
    private volatile String tagged, status, currentPop;
    private volatile int currentGen;
    
    public MAGIcForEnglish(File F, int ng, int ps, double pm) {
        f= F;
        numGen= ng;
        popSize= ps;
        Pm= pm;
        tagged= status= currentPop= null;
        currentGen=0;
        setProgress(0);
    }

    /**
     * @param args the command line arguments
     */
    @SuppressWarnings("ResultOfObjectAllocationIgnored")
    public static void main(String[] args)  {
        new MAGIcForEnglish(new File(args[0]), 20, 10, 0.007).execute();
    }

    @Override
    protected Void doInBackground() throws Exception {
        int stepSize= (int) Math.ceil(100.0/(4.0*numGen-2.0));
        Timer t= new Timer();
        setStatus("MAGIc implementation for English Language\nCalling Tagger...");
        System.out.print(status);
        try{
            // Calling Tagger
            POSTagger.tagger(f);
            setStatus("tagging completed.");
            System.out.println(status);
            setTagged(POSTagger.tSentences);
            setProgress(Math.min(100, getProgress()+stepSize));
            //MAGIc first stage: Initialize
            MAGIcComponents algo= new MAGIcComponents(popSize, Pm);
            //Begin execution
            setStatus("Initializing with Parameters.....");
            System.out.println(status+"\n Population Size: "
            +popSize+"\tMax Generations: "+numGen+"\tProbability of Mutation: "+Pm);
            algo.initialize();
            setStatus("Initial generation formed!");
            setCurrentPop(algo.population);
            setCurrentGen(currentGen+1);
            setProgress(Math.min(100, getProgress()+stepSize));
            while(currentGen<numGen)  {
                setStatus(status+"\nLocal Searching...");
                System.out.print("Generation "+currentGen+":\nLocal Searching...");
                t.reset();
                
                algo.improveAndEvaluate();
                
                setStatus("Local Searching...completed("+t.getElapsedTime()+" sec)\nMutating Grammars...");
                System.out.print("completed("+t.getElapsedTime()+" sec)\nMutating Grammars...");
                setProgress(Math.min(100, getProgress()+stepSize));
                t.reset();
                
                algo.mutate();
                
                setStatus("Mutating Grammars...completed("+t.getElapsedTime()+" sec)\nGeneralizing Grammars...");
                System.out.print("completed("+t.getElapsedTime()+" sec)\nGeneralizing Grammars...");
                setProgress(Math.min(100, getProgress()+stepSize));
                t.reset();
                
                algo.generalize();
                
                setStatus("Generalizing Grammars...completed("+t.getElapsedTime()+" sec)");
                System.out.print("completed("+t.getElapsedTime()+" sec)");
                setProgress(Math.min(100, getProgress()+stepSize));
                
                algo.select();
                
                setCurrentGen(currentGen+1);
                System.out.println("Generation advanced to "+currentGen);
                setCurrentPop(algo.population);
                setProgress(Math.min(100, getProgress()+stepSize));
            }
            System.out.println(currentPop);
        }
        catch(FileNotFoundException | MalformedGrammarException | TooManyLoopIterationsException e) {
            setStatus("Fatal Error! Thread exiting.");
            System.out.println(status);
            System.exit(-2);
        }
        return null;
    }

    private void setTagged(String tSentences) {
        firePropertyChange("tagged", tagged, tSentences);
        tagged= tSentences;
    }

    private void setCurrentGen(int i) {
        firePropertyChange("currentgen", currentGen, i);
        currentGen= i;
    }
    
    private void setStatus(String s)    {
        firePropertyChange("status", status, s);
        status= s;
    }

    private void setCurrentPop(ArrayList<Grammar> population) {
        StringBuilder newVal= new StringBuilder(500);
        int i= 1;
        for(Grammar g: population)  {
            newVal= newVal.append("Grammar ").append(i++)
                    .append(": (Fitness score: ").append(g.fitness)
                    .append(")\n");
            for(Rule r: g.rules)
                newVal= newVal.append(r.T.name).append(" --> ")
                        .append(r.returnRule()).append("\n");
            newVal= newVal.append("\n");
        }
        firePropertyChange("currentpop", currentPop, newVal.toString());
        currentPop= newVal.toString();
    }
}