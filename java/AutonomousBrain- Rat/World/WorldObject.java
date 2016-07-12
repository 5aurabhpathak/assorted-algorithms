/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package World;

/**
 *
 * @author Saurabh
 */
public abstract class WorldObject
{
    public int x, y;
    abstract public boolean isFood();
    abstract public boolean isSnake();
    abstract public boolean isWall();
    abstract public boolean isRat();
}