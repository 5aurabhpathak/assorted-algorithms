/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package magic.pkgfor.english.support;

import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author Saurabh
 */
public class POSTagger {
    
    public static ArrayList <String> tags= new ArrayList <>();
    public static String tSentences= "";
    
    public static void tagger(File f) throws FileNotFoundException  {
        //stanford log-linear pos tagger implementation
        ArrayList<TaggedWord> tSentence;
        MaxentTagger tagger= new MaxentTagger("C:\\Users\\Saurabh\\Documents\\My Working Set\\Study\\final year project\\stanford-postagger-full-2013-06-20\\models\\wsj-0-18-left3words-distsim.tagger");
        List<List<HasWord>> sentences = MaxentTagger.tokenizeText(new BufferedReader(new FileReader(f)));
        System.out.println("Read input from file at-- "+f.getAbsolutePath());
        for (List<HasWord> sentence : sentences) {
            tSentence = tagger.tagSentence(sentence);
            for(TaggedWord tw : tSentence)  {
                tags.add(tw.tag().toLowerCase());
                tSentences = tSentences.concat(tw.toString()+"  ");
            }
        }
        tags[5]= "kk-kkkk";
//        System.out.println(tags.toString());
    }
    
}