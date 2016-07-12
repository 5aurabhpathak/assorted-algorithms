/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package magic.pkgfor.english.support;

/**
 *
 * @author Saurabh
 */
public final class Timer {
    
    private long startTime;
    
    public Timer()  {
        reset();
    }
    
    public void reset()    {
        startTime= System.nanoTime();
    }
    
    public double getElapsedTime()   {
        return Math.round((System.nanoTime()-startTime)*Math.pow(10, -9)*1000.0)/1000.0;
    }
    
}
