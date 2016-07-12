/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package World;

import java.awt.Color;
import java.awt.Graphics;
import java.util.Collections;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import javax.swing.JPanel;
/**
 *
 * @author Saurabh
 */
public class RatWorld extends JPanel
{
    private static final long serialVersionUID = 1L;
    public static final List <WorldObject> objects= Collections.synchronizedList(new LinkedList <WorldObject>());
    public static boolean checkUnique(int x, int y)
    {
        if(getObject(x, y)==null)
            return true;
        else return false;
    }
    public static WorldObject getObject(int x, int y)
    {
        WorldObject wob;
        Iterator <WorldObject> it;
        synchronized(objects)
        {
            it= objects.iterator();
            while(it.hasNext())
            {
                wob= it.next();
                if((wob.x==x)&&(wob.y==y))
                    return wob;
            }
        }
        return null;
    }
    public static void destroyObject(WorldObject target)
    {
        WorldObject wob;
        Iterator <WorldObject> it;
        synchronized(objects)
        {
            it= objects.iterator();
            while(it.hasNext())
            {
                wob= it.next();
                if(wob.equals(target))
                {
                    it.remove();
                    break;
                }
            }
        }
    }
    @Override
    public void paintComponent(Graphics g)
    {
        WorldObject wob;
        Iterator <WorldObject> it;
        g.setColor(Color.green);
        g.fillRect(0, 0, this.getWidth(), this.getHeight());
        synchronized(objects)
        {
            it= objects.iterator();
            while(it.hasNext())
            {
                wob= it.next();
                if(wob.isFood())
                {
                    g.setColor(Color.green);
                    g.fillOval(wob.x, wob.y, 10, 10);
                }
                else
                {
                    if(wob.isSnake())
                        g.setColor(Color.black);
                    else if(wob.isRat())
                        g.setColor(Color.ORANGE);
                    else
                        g.setColor(Color.red);
                    g.fillRect(wob.x, wob.y, 10, 10);
                }
            }
        }
    }
}