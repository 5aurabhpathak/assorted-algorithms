/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package COI;

import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;

/**
 *
 * @author phoenix
 */
final class KNNClassifier extends SupervisedClassifier {
    
    int k;
    
    KNNClassifier(String train, int kmean) throws IOException {
        k = kmean;
        trainSet = DataSet.createSet(train);
    }

    @Override
    String classify(double[] ftstvector) {
        HashMap<Double, double[]> diffs = new HashMap<>();
        double[] diffarr = new double[trainSet.size];
        int i = 0;
        for (double[] ftrnvector : trainSet.iris.keySet()) {
            diffarr[i] = Operations.calcDist(ftstvector, ftrnvector);
            diffs.put(diffarr[i++], ftrnvector);
        }
        return chooseNeighbour(diffs, diffarr, k);
    }

    private String chooseNeighbour(HashMap<Double, double[]> diffs, double[] diffarr, int i) {
        double[] kminarr = Operations.kMin(diffarr, i);
        HashMap<String, Integer> classescount = new HashMap<>();
        for (double d : kminarr) {
            int PrevCnt = classescount.getOrDefault(trainSet.iris.get(diffs.get(d)), 0);
            if (PrevCnt == 0) {
                classescount.put(trainSet.iris.get(diffs.get(d)), 1);
            } else {
                classescount.replace(trainSet.iris.get(diffs.get(d)), ++PrevCnt);
            }
        }
        Iterator<String> it = classescount.keySet().iterator();
        int max = 0;
        String prediction = null;
        while (it.hasNext()) {
            String key = it.next();
            int val = classescount.get(key);
            if (val > max) {
                max = val;
                prediction = key;
            }
        }
        return prediction;
    }
    
}
