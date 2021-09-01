/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package COI;
import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import javax.swing.SwingWorker;

/**
 *
 * @author phoenix
 */
public final class Main extends SwingWorker <Void, Void>  {

    Classifier cf;
    volatile String status;
    
    Main(Classifier c)   {
        cf = c;
        status = "";
    }
    
    /**
     * @param args
     * @throws java.io.IOException
     * @paramHashtable t; args the command line arguments
     */
    public static void main(String[] args) throws IOException, Exception {
        new Main(new FCMClassifier(3, 3, 0.0)).doInBackground();
    }

    @Override
    protected Void doInBackground() throws Exception {
        setStatus("Classifying data set using fuzzy c-means...");
        
        DataSet dataSet = DataSet.createSet("/home/phoenix/src/java/iris22/bezdekIris.data");
        
        HashMap<double[], String> classified = cf.classify(dataSet);
        System.out.println("Feature vector\t\t\t\t\t\t\t\t\t\t\t\t\t\tIn cluster\t\t\t\tOriginal (for comparison)");
        for (double [] d : dataSet.iris.keySet())  {
            Operations.display(d);
            System.out.println("\t\t\t\t" + classified.get(d) + "\t\t\t\t" + dataSet.iris.get(d));
        }
        
        //supervised classifier error checker
        /*Iterator<double[]> itst = dataSet.iris.keySet().iterator(),
                iclass = classified.keySet().iterator();
        double wrong = 0;
        String s1, s2;
        while (itst.hasNext()) {
            s1 = dataSet.iris.get(itst.next());
            s2 = classified.get(iclass.next());
            if (!s1.matches(s2)) {
                wrong++;
                setStatus("Wrongly classified " + s1 + " as " + s2);
            }
        }
        setStatus("Percentage accuracy:" + ((classified.size() - wrong) / classified.size() * 100));*/
        
        return null;
    }
    
    //GUI specific code
    private void setStatus(String s) {
        System.out.println(s);
        firePropertyChange("status", status, status + "\n" + s);
        status += "\n" + s;
    }
    
}