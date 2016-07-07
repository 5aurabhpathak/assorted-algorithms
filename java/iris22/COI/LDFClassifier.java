/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package COI;

import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;

/**
 *
 * @author phoenix
 */
final class LDFClassifier extends SupervisedClassifier {
    
    HashMap <String, Function> funcs;
    double eta;
    private LDFClassifier() {}
    
    static LDFClassifier getClassifier(String trainfile, double eta) throws IOException    {
        LDFClassifier ldf = new LDFClassifier();
        ldf.trainSet = DataSet.createSet(trainfile);
        ldf.eta = eta;
        double[] wt;
        double i = 0;
        ldf.funcs = new HashMap();
        for (String f : ldf.trainSet.classlbls) {
            wt = new double[ldf.trainSet.dimensions];
            Arrays.fill(wt, i);
            Function func = new Function(wt);
            ldf.funcs.put(f, func);
        }
        ldf.stabilize();
        return ldf;
    }

    private void stabilize() {
        for (double[] vector : trainSet.iris.keySet())
            for (int epoch = 1; epoch <= 2000; epoch++) {
                String prediction = classify(vector),
                        actual = trainSet.iris.get(vector);
                if(prediction.matches(actual))
                    break;
                else
                    adjustParameters(actual, prediction, vector);
            }
    }

    private void adjustParameters(String actual, String prediction, double [] vector) {
        funcs.get(actual).update(vector, eta, false); //increment
        funcs.get(prediction).update(vector, eta, true); //decrement
    }

    @Override
    String classify(double[] vector) {
        double max = Double.NEGATIVE_INFINITY;
        String prediction = null;
        for(String c : funcs.keySet())   {
            double value = funcs.get(c).value(vector);
            if(Double.compare(value, max) > 0) {
                max = value;
                prediction = c;
            }
        }
        System.out.println(max);
        return prediction;
    }
    
}

final class Function {

    double[] a;

    Function(double[] w) {
        a = w;
    }

    double value(double[] vector) {
        double sum = 0.0;
        int i;
        for (i = 0; i < vector.length; i++) {
            sum += a[i] * vector[i];
        }
        return sum;// + a[i];
    }

    void update(double[] vector, double eta, boolean dec) {
        int i;
        for (i = 0; i < vector.length; i++) {
            if (dec == true) {
                a[i] = a[i] - Math.abs(eta * vector[i]);
            } else {
                a[i] = a[i] + Math.abs(eta * vector[i]);
            }
        }
//        if (dec == true) {
//            a[i] = a[i] - Math.abs(eta * a[i]);
//        } else {
//            a[i] = a[i] + Math.abs(eta * a[i]);
//        }
    }

}
