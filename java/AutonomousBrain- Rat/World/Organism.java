/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package World;

import java.util.LinkedList;
import java.util.Random;

/**
 *
 * @author Saurabh
 */
public abstract class Organism extends WorldObject
{
    WorldObject[] radar= new WorldObject[8];
    int energy, goal= 1, lastdir= 8, eating= 0;
    long speed;
    public String name;
    WorldObject Northvalue, Eastvalue, Southvalue, Westvalue, NEvalue, SWvalue, SEvalue, NWvalue, target;
    public void setRadar(int xpos, int ypos)
    {
        Northvalue= RatWorld.getObject(x, y-10);
        Eastvalue= RatWorld.getObject(x+10, y);
        Southvalue= RatWorld.getObject(x, y+10);
        Westvalue= RatWorld.getObject(x-10, y);
        NEvalue= RatWorld.getObject(x+10, y-10);
        SEvalue= RatWorld.getObject(x+10, y+10);
        SWvalue= RatWorld.getObject(x-10, y+10);
        NWvalue= RatWorld.getObject(x-10, y-10);
    }
    public WorldObject [] readRadar()
    {
        radar[0]= Northvalue;
        radar[1]= NEvalue;
        radar[2]= Eastvalue;
        radar[3]= SEvalue;
        radar[4]= Southvalue;
        radar[5]= SWvalue;
        radar[6]= Westvalue;
        radar[7]= NWvalue;
        return radar;
    }
    public void setPosition(int direction)
    {
        switch(direction)
        {
            case 0: y-=10; break;
            case 2: x+=10; break;
            case 4: y+=10; break;
            case 6: x-=10; break;
            case 1: x+=10;
                    y-=10;  break;
            case 3: x+=10;
                    y+=10;  break;
            case 5: x-=10;
                    y+=10;  break;
            case 7: x-=10;
                    y-=10;  break;
        }
        World.MainClass.window.repaint();
    }
    public int chooseDirection()
    {
        int i;
        Random r= new Random();
        LinkedList <Integer> choices= new LinkedList<>();
        for(i=0; i<8; i++)
            if((lastdir!=i)&&(radar[i]==null))
                choices.add(i);
        try
        {
            return choices.get(r.nextInt(choices.size()));
        }
        catch(IllegalArgumentException e)
        {
            return 8;
        }
    }
    public void rest()
    {
//        System.out.println("Will rest");
        setPosition(8);
        energy--;
        if(energy==0)
            energy=150;
    }
    abstract public void moveToFood()throws InterruptedException;
    abstract public void generateGoal();
    abstract public void achieve();
    abstract public int containsFood();
    abstract public void eat();
}