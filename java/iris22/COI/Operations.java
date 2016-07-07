/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package COI;

import java.util.Arrays;

/**
 *
 * @author phoenix
 */
class Operations {
    
    static private int set;
    
    static double colMean(double [][] data, int i)    {
        double sum = colSum(data, i);
        return sum/data.length;
    }
    
    static double colSd(double [][] data, int j)   {
        double xminusmeansquare = 0;
        double meanval = colMean(data, j);
        for(int i = 0; i < data.length; i++)
            xminusmeansquare += Math.pow((data[i][j] - meanval), 2.0);
        return Math.sqrt(xminusmeansquare / data.length);
    }
    
    static void display(double [] data) {
        for(double d : data)
            System.out.print(d + "\t");
    }

    static double calcDist(double[] ftstvector, double[] ftrnvector) {
        double sum = 0;
        for(int i = 0; i < ftstvector.length; i++)
            sum += Math.pow((ftstvector[i] - ftrnvector[i]), 2.0);
        return Math.sqrt(sum);
    }

    static double [] kMin(double[] diffarr, int k) {
        Arrays.parallelSort(diffarr);
        return Arrays.copyOf(diffarr, k);
    }

    static double colSum(double [][] d, int i) {
        double sum = 0;
        for (int j = 0; j < d.length; j++)
            sum += d[j][i];
        return sum;
    }
    
    static int indexOfMax(double [] d)   {
        int i = 0;
        double max = d[0];
        for (int j = 1; j < d.length; j++)
            if (d[j] > max) {
                max = d[j];
                i = j;
            }
        return i;
    }
    
}
