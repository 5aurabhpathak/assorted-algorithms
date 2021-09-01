/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package Brain;

import World.Organism;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Saurabh
 */
public class Eyes implements Runnable
{
    Organism o;
    public Eyes(Organism org)
    {
        o= org;
    }
    public void run()
    {
        while(true)
        {
            o.setRadar(o.x, o.y);
            try {
                Thread.sleep(100);
            } catch (InterruptedException ex) {
                Logger.getLogger(Eyes.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }
}
