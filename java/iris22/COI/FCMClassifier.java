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
public final class FCMClassifier extends Classifier {
    double m, e, J, mew[][], centers[][];
    int c;

    public FCMClassifier(double M, int C, double eps) {
        m = M;
        e = eps;
        c = C;
    }

    private void initMatrix() {
        for (int i = 0; i < mew.length; i++)  {
            double sum = 0;
            double [] temp = new double[mew[0].length];
            for (int j = 0; j < mew[0].length; j++)  {
                temp[j] = Math.random();
                sum += temp[j];
            }
            for (int j = 0; j < mew[0].length; j++)
                mew[i][j] = temp[j] / sum;  //mew of ith vector from jth cluster
        }
    }

    @Override
    HashMap<double[], String> classify(DataSet testSet) {
        mew = new double[testSet.size][c];
        initMatrix();
        centers = new double[c][testSet.dimensions];
        double Jprime = 0;
        do {
            J = Jprime;
            calcCenters(testSet);
            calcMew(testSet);
            Jprime = calcJ(testSet);
        } while (Math.abs(J - Jprime) < e);
        J = Jprime;
        
        HashMap<double[], String> result = new HashMap<>();
        for (int i = 0; i < testSet.size; i++)
            result.put(testSet.feat[i], String.valueOf(Operations.indexOfMax(mew[i]) + 1));
        return result;
    }

    private void calcCenters(DataSet testSet) {
        for (int j = 0; j < c; j++) {
            double denominator = Operations.colSum(mew, j);
            for (int d = 0; d < testSet.dimensions; d++) {
                double numerator = 0;
                for (int i = 0; i < testSet.size; i++) {
                    numerator += Math.pow(mew[i][j], m) * testSet.feat[i][d];
                }
                centers[j][d] = numerator / denominator;
            }
        }
    }

    private void calcMew(DataSet testSet) {
        for (int i = 0; i < testSet.size; i++) {
            for (int j = 0; j < c; j++) {
                double sum = 0, dij = Operations.calcDist(testSet.feat[i], centers[j]);
                for (int k = 0; k < c; k++) {
                    sum += Math.pow(dij / Operations.calcDist(testSet.feat[i], centers[k]), 2 / (m - 1));
                }
                mew[i][j] = 1 / sum;
            }
        }
    }

    private double calcJ(DataSet testSet) {
        double sum = 0;
        for (int i = 0; i < testSet.size; i++) {
            double innersum = 0;
            for (int j = 0; j < c; j++) {
                double dijsquare = Math.pow(Operations.calcDist(testSet.feat[i], centers[j]), 2.0);
                innersum += Math.pow(mew[i][j], m) * dijsquare;
            }
            sum += innersum;
        }
        return sum;
    }
}
