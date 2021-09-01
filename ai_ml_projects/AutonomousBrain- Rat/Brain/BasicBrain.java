/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package Brain;

import World.Organism;

/**
 *
 * @author Saurabh
 */
public class BasicBrain implements Runnable
{
    Organism o;
    public BasicBrain(Organism org)
    {
        this.o= org;
    }
    @Override
    public void run()
    {
//        System.out.println("Rat BasicBrain began execution");
        new Thread(new Eyes(o), "Eyes of "+o.name).start();
        new Thread(new GoalGen(o), "Goals of"+o.name).start();
        new Thread(new Ac)
    }
}