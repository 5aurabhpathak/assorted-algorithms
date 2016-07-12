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
public final class Rat extends Organism
{
    public Rat(String name, int x, int y)
    {
        this.name= name;
        this.x= x;
        this.y= y;
        this.energy= 150;
        this.speed= 500;
        this.setRadar(x, y);
    }
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
        return false;
    }
    @Override
    public boolean isRat()
    {
        return true;
    }
    public void generateGoal()
    {
        int i;
        radar= readRadar();
//            System.out.println("Name: "+rat.name+"current energy: "+rat.energy);
//            System.out.println("radar: "+radar[0]+radar[1]+radar[2]+radar[3]+radar[4]+radar[5]+radar[6]+radar[7]+
//                    "\nx= "+rat.x+" y= "+rat.y);
        if((energy<151)&&(goal!=3))
            goal=2;
        else if(energy>750)
            goal=1;
        for(i=0; i<8; i++)
            if((radar[i]!=null)&&(radar[i].isSnake()))
            {
                goal=4;
//                System.out.println(name+" saw snake and is afraid.");
                break;
            }
    }
    public void achieve()
    {
//        System.out.println("Working for goal "+goal);
        switch(goal)
        {
            case 1:rest();   break;
            case 2: try
                    {
                        moveToFood();
                    } 
                    catch (InterruptedException ex)
                    {
                        Logger.getLogger(Rat.class.getName()).log(Level.SEVERE, null, ex);
                    }   break;
            case 3: eat();  break;
            case 4: runForLife();   break;
        }
    }
    public int containsFood()
    {
        int i;
        for(i=0; i<8; i++)
            if((radar[i]!=null)&&(radar[i].isFood()))
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
        Thread.sleep(speed);
        if((res!=-1)&&(lastdir!=res))
        {
            dir= res;
            setPosition(dir);
            goal= 3;
            System.out.println(name+" found food.");
        }
        else
        {
            dir= chooseDirection();
            setPosition(dir);
        }
        lastdir= (dir+4)%8;
    }
    public void eat()
    {
        rest();
        eating+=25;
//        System.out.println(name+" ate "+eating+"% food.");
        if(eating==100)
        {
            eating=0;
            RatWorld.destroyObject(target);
            World.MainClass.window.repaint();
            energy=1000;
            goal= 1;
//            System.out.println(name+" says Burp!");
        }
    }
    private void runForLife()
    {
        int i;
        try
        {
            Thread.sleep(speed);
            for(i=0; i<8; i++)
                if((radar[i]!=null)&&(radar[i].isSnake()))
                {
                    if(movable((i+4)%8))
                        setPosition((i+4)%8);
                    else if(movable((i+3)%8))
                        setPosition((i+3)%8);
                    else if(movable((i+5)%8))
                        setPosition((i+5)%8);
                    else if(movable((i+2)%8))
                        setPosition((i+2)%8);
                    else if(movable((i+6)%8))
                        setPosition((i+6)%8);
                    else if(movable((i+1)%8))
                        setPosition((i+1)%8);
                    else if(movable((i+7)%8))
                        setPosition((i+7)%8);
                    else rest();
                    break;
                }
//            System.out.println(name+" ran away from a snake. Is happy!");
        }
        catch(NullPointerException e)
        {
            System.out.println("Rat was bitten by a snake. Rat is dead.");
        }
        catch(InterruptedException e){}
    }
    private boolean movable(int i)
    {
        if((lastdir!=i)&&(radar[i]==null))
        {
            lastdir= (i+4)%8;
            return true;
        }
        else return false;
    }
}