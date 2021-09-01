/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package COI;

import java.util.HashMap;

/**
 *
 * @author phoenix
 */
abstract class SupervisedClassifier extends Classifier {
    
    DataSet trainSet;
    
    @Override
    HashMap<double[], String> classify(DataSet testSet) {
        HashMap<double[], String> classified = new HashMap<>();
            for (double[] tstvector : testSet.iris.keySet()) {
                classified.put(tstvector, classify(tstvector));
            }
            return classified;
    }
    
    abstract String classify(double [] tstvector);
    
}
