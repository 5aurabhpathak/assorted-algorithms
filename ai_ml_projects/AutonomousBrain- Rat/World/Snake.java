/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package World;

import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Saurabh
 */
public final class Snake extends Organism
{
    @Override
    public boolean isFood()
    {
        return false;
    }
    @Override
    public boolean isWall()
    {
        return false;
    }
    @Override
    public boolean isSnake()
    {
        return true;
    }
    @Override
    public boolean isRat()
    {
        return false;
    }
    public Snake(String name, int x, int y)
    {
        this.name= name;
        this.x= x;
        this.y= y;
        this.energy= 750;
        this.speed= 1000;
        this.setRadar(x, y);
    }
    public void generateGoal()
    {
        radar= readRadar();
//            System.out.println("Name: "+rat.name+"current energy: "+rat.energy);
//            System.out.println("radar: "+radar[0]+radar[1]+radar[2]+radar[3]+radar[4]+radar[5]+radar[6]+radar[7]+
//                    "\nx= "+x+" y= "+y);
        if((energy<751)&&(goal!=3))
            goal=2;
    }
    public void achieve()
    {
        switch(goal)
        {
            case 1:rest(); break;
            case 2:try
                   {
                       moveToFood();
                   } catch (InterruptedException ex)
                   {
                       Logger.getLogger(Snake.class.getName()).log(Level.SEVERE, null, ex);
                   }    break;
            case 3:eat();
        }
    }
    public int containsFood()
    {
        int i;
        for(i=0; i<8; i++)
            if((radar[i]!=null)&&(radar[i].isRat()))
            {
                target= radar[i];
                return i;
            }
        return -1;
    }
    public void moveToFood()throws InterruptedException
    {
        int res= containsFood(), dir;
//        System.out.print(res);
        if((res!=-1)&&(lastdir!=res))
        {
            dir= res;
            setPosition(dir);
            System.out.println(name+" found "+((Organism)target).name);
            if((x==target.x)&&(y==target.y))
            {
                synchronized(target)
                {
                    System.out.println(name+" killed "+((Organism)target).name);
                    RatWorld.destroyObject(target);
                }
                World.MainClass.window.repaint();
                while(!MainClass.orgs.remove((Organism)target));
                goal=3;
            }
            else
            {
                System.out.println(((Organism)target).name+" ran away.");
            }
        }
        else
        {
            dir= chooseDirection();
            setPosition(dir);
        }
        lastdir= (dir+4)%8;
        Thread.sleep(speed);
    }
    public void eat()
    {
        rest();
        if(eating==500)
        {
            eating=0;
            energy=10000;
            goal= 1;
//            System.out.println(name+" says Burp!");
        }
//        else
//        {
//            System.out.println(name+" ate "+eating/5+"% food.");
//        }
        else eating+=25;
    }
}
