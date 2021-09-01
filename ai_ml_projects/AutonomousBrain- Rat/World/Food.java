/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package World;

/**
 *
 * @author Saurabh
 */
public class Food extends WorldObject
{
    @Override
    public boolean isFood()
    {
        return true;
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
        return false;
    }
    public Food(int xpos, int ypos)
    {
        x= xpos;
        y= ypos;
    }
}
