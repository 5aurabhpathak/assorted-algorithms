/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package COI;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.LineNumberReader;
import java.util.HashMap;

/**
 *
 * @author phoenix
 */
class DataSet {
    
    int dimensions, size;
    double [][] feat;
    String [] classlbls;
    HashMap < double [], String> iris;
    
    private DataSet()   {}
    
    //private method to count number of samples and dimentionality of the
    //training set from file
    private void getlimits(String fname) throws IOException {
        String[] tokens;
        //this might fail for file with more than 32k lines as getlinenumber()
        //returns an int.
        LineNumberReader lnr = new LineNumberReader(
                new FileReader(fname));
        tokens = lnr.readLine().split(",");
        dimensions = tokens.length - 1;
        lnr.skip(Long.MAX_VALUE);
        size = lnr.getLineNumber();
        lnr.close();
    }
    
    //reads from file and creates a normalized training set
    public static DataSet createSet(String fname) throws IOException {
        String s, tokens[];
        int i, j = 0;
        DataSet obj = new DataSet();
        obj.getlimits(fname);
        obj.iris = new HashMap<>();
        BufferedReader fr = new BufferedReader(new FileReader(fname));
        obj.feat = new double[obj.size][obj.dimensions];
        obj.classlbls = new String[obj.size];
        while ((s = fr.readLine()) != null) {
            tokens = s.split(",");
            for (i = 0; i < tokens.length - 1; i++)
                obj.feat[j][i] = Double.parseDouble(tokens[i]);
            obj.classlbls[j++] = tokens[i];
        }
        fr.close();
        for(i = 0; i < obj.dimensions; i++) {
            double meanv = Operations.colMean(obj.feat, i),
                    sdv = Operations.colSd(obj.feat, i);
            for (j = 0; j < obj.size; j++) {
                obj.feat[j][i] = (obj.feat[j][i] - meanv) / sdv;
            }
        }
        for (i = 0; i < obj.size; i++)
            obj.iris.put(obj.feat[i], obj.classlbls[i]);
        return obj;
    }
    
    public void displaySet() {
        for (double [] d : iris.keySet()) {
            Operations.display(d);
            System.out.println(iris.get(d));
        }
    }
        
}