/*
 * current progress/synopsis: today I implemented snake brain. Snakes are now alive!
 *      Introduced speed factor into the world. though giving rise to some new bugs.
 * known bugs: snakes get trapped between food!
 *             rat's ghost still active when the rat is killed by a snake!(bug removed)
 *             snake kills a rat and reports that it ate it. still dead bodies remain!(bug removed)
 *             slow snakes never manage to kill a single fast moving rat! Not what we see
 * in real world.
 */
package World;

import Brain.BasicBrain;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Random;
import javax.swing.JFrame;

/**
 *
 * @author Saurabh
 */
public class MainClass
{
    static Random r= new Random();
    public static HashSet <Organism> orgs= new HashSet<>();
    public static JFrame window= new JFrame("Basic Rat Behaviour Simulation");
    public static RatWorld rw= new RatWorld();
    @SuppressWarnings("ResultOfObjectAllocationIgnored")
    public static void main(String args[])throws InterruptedException
    {
        Iterator <Organism> it;
        BasicBrain ap;
        Organism o;
        window.add(rw);
        window.setSize(716, 638);
        window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        window.setVisible(true);
        initFood(rw, 0);
        initSnake(rw, 0);
        initWalls(rw);
        initRat(rw, 1);
        it= orgs.iterator();
        Thread.sleep(2000);
        while(it.hasNext())
        {
            o= it.next();
            ap= new BasicBrain(o);
//            Thread.sleep(3000);
            new Thread(ap, "Brain Thread for "+o.name).start();
        }
    }
    @SuppressWarnings("ValueOfIncrementOrDecrementUsed")
    private static void initFood(RatWorld rw, int numfood)
    {
        int i=0, exp, x, y;
        while(i++<numfood)
        {
            exp= r.nextInt(rw.getWidth()-20)+10;
            x= (exp%10==0) ? exp : exp/10*10;
            exp= r.nextInt(rw.getHeight()-20)+10;
            y= (exp%10==0) ? exp : exp/10*10;
            RatWorld.objects.add(new Food(x, y));
        }
    }
    private static void initSnake(RatWorld rw, int numsnake)
    {
        int exp, x, y, i=0;
        Snake snake;
        while(i++<numsnake)
        {
            exp= r.nextInt(rw.getWidth()-20)+10;
            x= (exp%10==0) ? exp : exp/10*10;
            exp= r.nextInt(rw.getHeight()-20)+10;
            y= (exp%10==0) ? exp : exp/10*10;
            if(RatWorld.checkUnique(x, y))
            {
                snake= new Snake("Snake @ "+x+", "+y, x, y);
                RatWorld.objects.add(snake);
                orgs.add(snake);
            }
            else i--;
        }
    }
    private static void initWalls(RatWorld rw)
    {
        int maxx= rw.getWidth(), maxy= rw.getHeight(), x=0;
        while(x<maxx)
        {
            RatWorld.objects.add(new Wall(x, 0));
            RatWorld.objects.add(new Wall(x, maxy-10));
            x+=10;
        }
        x=10;
        while(x<maxy-10)
        {
            RatWorld.objects.add(new Wall(0, x));
            RatWorld.objects.add(new Wall(maxx-10, x));
            x+=10;
        }
    }
    private static void initRat(RatWorld rw, int numrats)
    {
        int exp, x, y, i=0;
        Rat rat;
        while(i++<numrats)
        {
            exp= r.nextInt(rw.getWidth()-20)+10;
            x= (exp%10==0) ? exp : exp/10*10;
            exp= r.nextInt(rw.getHeight()-20)+10;
            y= (exp%10==0) ? exp : exp/10*10;
            if(RatWorld.checkUnique(x, y))
            {
                rat= new Rat("Rat @ "+x+", "+y,x, y);
                RatWorld.objects.add(rat);
                orgs.add(rat);
            }
            else i--;
        }
//        System.out.println("New Rat formed at location "+rat.x+", "+rat.y);
    }
}