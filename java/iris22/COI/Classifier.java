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
abstract class Classifier {
    abstract HashMap<double[], String> classify(DataSet testSet);
}