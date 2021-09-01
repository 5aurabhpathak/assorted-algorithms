/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package World;

/**
 *
 * @author Saurabh
 */
public class Wall extends WorldObject
{
    @Override
    public boolean isFood()
    {
        return false;
    }
    @Override
    public boolean isWall()
    {
        return true;
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
    public Wall(int xpos, int ypos)
    {
        x= xpos;
        y= ypos;
    }
}
