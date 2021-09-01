/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package GA;

/**
 *
 * @author Saurabh
 */
public class Function {
    
    static double F(double x, double y)    {
        double r = 6.0 - Math.pow(x, 2) - Math.pow(y, 2);
        if (r > 6.0)    {
            System.out.println(x + ">>>>>>" + y);
            System.exit(1);
        }
        return r;
    }
    
}