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
public class GoalGen implements Runnable
{
    Organism o;
    public GoalGen(Organism org)
    {
        o= org;
    }
    public void run()
    {
        o.generateGoal();
        try {
            Thread.sleep(500);
        } catch (InterruptedException ex) {
            Logger.getLogger(GoalGen.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
}
