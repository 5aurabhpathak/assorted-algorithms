/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package GA;

import java.nio.ByteBuffer;
import java.text.DecimalFormat;
import java.util.Arrays;
import java.util.Map.Entry;
import java.util.Objects;
import java.util.Random;
import java.util.TreeMap;

/**
 *
 * @author Saurabh
 */
public class GAmain {

    TreeMap <Double, boolean[]> population, rouletteWheel;
    final int size;
    final double Pm, Pc;
    double avgFitness, maxFitness, delta;
    final long generations;
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        GAmain ga = new GAmain(30, 0.03, 0.3, 100, 0.01); //poolsize, um, ux, gen, e
       // boolean[] ex = ga.encode(-19.378711, 11.0241);
//        ga.displayPop();
        //for (long i = 0; i < ga.generations; i++)    {
        double difference;
        do  {
            double oldAvg = ga.avgFitness;
            ga.mutate();
            ga.crossover();
            ga.maxFitness = ga.population.lastKey();
            difference = Math.abs(oldAvg - ga.avgFitness);
//            ga.displayPop();
        } while (difference > ga.delta);
        Entry <Double, boolean[]> e = ga.population.lastEntry();
        ByteBuffer buff = ByteBuffer.wrap(byteArray(e.getValue()));
        System.out.println("Fittest:\nx = " + buff.getDouble() + "\ny = " +
                buff.getDouble() + "\nF(x, y) = " + ga.maxFitness);
//        buff = ByteBuffer.wrap(byteArray(ex));
//        System.out.println("Test: x1: " + buff.getDouble() + "\ty1: " + buff.getDouble()
//            + "\nF1,1 :" + Function.F(0.0, 0.0));
    }

    private GAmain(int s, double pm, double pc, long g, double d) {
        population = new TreeMap<>();
        size = s;
        Pm = pm;
        Pc = pc;
        delta = d;
        generations = g;
        avgFitness = 0;
        maxFitness = 0;
        rouletteWheel = new TreeMap<>();
        initializePop(s);
    }

    private void displayPop() {
        ByteBuffer buff;
        for (double d : population.keySet())   {
            buff = ByteBuffer.wrap(byteArray(population.get(d)));
            System.out.println(buff.getDouble() + ", " + buff.getDouble()
                                + "\tFitness: " + d);
        }
    }

    private void initializePop(int s) {
        for (int i = 0; i < s; i++)   {
            double x = Math.random() * 100, y = Math.random() * 100,
                    z = Function.F(x, y);
            population.put(z, encode(x, y));
            avgFitness += z;
        }
        avgFitness /= s;
    }

    private boolean[] encode(double x, double y) {
        ByteBuffer buff = ByteBuffer.allocate(16);
        buff.putDouble(x);
        buff.putDouble(y);
        byte [] b = buff.array();
        return booleanArray(b);
    }

    private void crossover() {
        TreeMap <Double, boolean[]> newGen = new TreeMap<>();
        avgFitness = 0;
        //elitist approach-- find n fittest chromosomes
        for (int i = 0; i < 2; i++) {
            Entry<Double, boolean[]> e = population.pollLastEntry();
            newGen.put(e.getKey(), e.getValue());
        }
        createRouletteWheel();
        System.out.println("crossover");
        while(newGen.size() < size)    {
            //select two chromosomes-- spin the roulette wheel
            Entry<Double, boolean[]> p1 = selectParent(newGen);
            if (newGen.size() == size)
                break;
            boolean [] parent1 = p1.getValue();
            Entry <Double, boolean[]> p2;
            do  {
                p2 = selectParent(newGen);
                if (newGen.size() == size) {
                    break;
                }
                System.out.println("select " + p2.getKey());
            } while (Objects.equals(p1.getKey(), p2.getKey()));   //to avoid mating with itself
            boolean [] parent2  = p2.getValue();
            Random rand = new Random();
            int location = rand.nextInt(128); //location of crossover
            boolean [] segment = Arrays.copyOf(parent1, location);
            System.arraycopy(parent2, 0, parent1, 0, location);
            System.arraycopy(segment, 0, parent2, 0, location);
            ByteBuffer buff = ByteBuffer.wrap(byteArray(parent1));
            double z = Function.F(buff.getDouble(), buff.getDouble());
            if (z != Double.NEGATIVE_INFINITY)
            //System.out.println("nnnnnnnnnnnnnn0nnnnnnnnnnn" + parent2.length);
            //if (
            newGen.put(z, parent1);// != null)    {
//                System.err.println("Fuck" + location);
//                System.exit(1);
//            }
            avgFitness += z;
            if (newGen.size() == size)
                break;
            //System.out.println("nnnnnnnnnnnnnn1nnnnnnnnnnn" + newGen.size());
            buff = ByteBuffer.wrap(byteArray(parent2));
            z = Function.F(buff.getDouble(), buff.getDouble());
            if (z != Double.NEGATIVE_INFINITY)
            //if (
            newGen.put(z, parent2);// != null) {
//                System.err.println("Fuck " + location);
//                System.exit(2);
//            }
            avgFitness += z;
            //System.out.println("nnnnnnnnnnnnn2nnnnnnnnnnnn" + newGen.size());
        }
        population = newGen;
        avgFitness /= size;
    }

    private Entry <Double, boolean[]> selectParent(TreeMap<Double, boolean[]> newGen) {
        Entry<Double, boolean[]> p;
        boolean flag;
        do {
            flag = false;
            double r = Math.random();
            p = rouletteWheel.floorEntry(r);
            r = Math.random();
            if (r < Pc) {
                newGen.put(p.getKey(), p.getValue());
                avgFitness += p.getKey();
                population.remove(p.getKey());
                createRouletteWheel();
                flag = true;
            }
        } while (flag);
        return p;
    }

    private void mutate()   {
        Random rand = new Random();
        TreeMap<Double, boolean[]> mutGen = new TreeMap<>();
        avgFitness = 0;
        System.out.println("===============" + population.size());
        for (double d : population.keySet())    {
            double r = Math.random();
            boolean [] b = population.get(d);
            if (r <= Pm)    {
                int pos = rand.nextInt(128);
                b[pos] = !b[pos];
                ByteBuffer buff = ByteBuffer.wrap(byteArray(b));
                double z = Function.F(buff.getDouble(), buff.getDouble());
                if (z != Double.NEGATIVE_INFINITY)  {
                    mutGen.put(z, b);
                    avgFitness += z;
                }
                else    {
                    mutGen.put(d, b);
                    avgFitness += d;
                }
            }
            else    {
                mutGen.put(d, b);
                avgFitness += d;
            }
        }
        population = mutGen;
        System.out.println("----------------"+mutGen.size());
        avgFitness /= size;
    }

    private static byte[] byteArray(boolean[] b) {
        byte[] returned = new byte[16];
        for (int i = 0; i < 16; i++) {
            for (int j = 0; j < 8; j++) {
                returned[i] |= (b[i * 8 + j] ? 1 : 0) << (7 - j);
            }
        }
        return returned;
    }

    private static boolean[] booleanArray(byte[] b) {
        boolean[] s = new boolean[128];
        for (int i = 0; i < 128; i++) {
            s[i] = (b[i / 8] & (1 << (7 - i % 8))) != 0;
        }
        return s;
    }

    private void createRouletteWheel() {
        rouletteWheel.clear();
        double sum = 0.0, rW = 0.0, smallest;
        boolean flag = false;
        DecimalFormat df = new DecimalFormat("#.####");
        df.setMaximumFractionDigits(5);
        if ((smallest = population.firstKey()) < 0) {
            flag = true;
        }
        for (double d : population.keySet()) {
            double fd = Double.parseDouble(df.format(d));
            if (flag) {
                fd -= smallest;
            }
            sum += fd;
            sum = Double.parseDouble(df.format(sum));
        }
        System.out.println("Sum: " + sum);
        for (double d : population.keySet()) {
            System.out.println(rW + "-->>" + d + "-----" + rouletteWheel.size());
            rouletteWheel.put(rW, population.get(d));
            double fd = Double.parseDouble(df.format(d));
            if (flag) {
                fd -= smallest;
            }
            rW += fd / sum;
            rW = Double.parseDouble(df.format(rW));
        }
    }

}