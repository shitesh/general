import au.com.bytecode.opencsv.CSVWriter;
import edu.uci.ics.crawler4j.url.WebURL;

import java.io.FileWriter;
import java.io.IOException;


/* class to keep track of all the urls that were discovered. This will save the url in a file in format
        URL, URLType
        where URLType = OK (within the school)
                        USC (not in the specific school but within USC)
                        outUSC (outside of USC)
*/
public class URLDiscovered {

    private CSVWriter csvWriter;
    private final String fileLocation = "output/urls.csv";
    private final String department = "arch.usc.edu";
    private final String school = "usc.edu";

    public URLDiscovered() throws IOException{
        csvWriter = new CSVWriter(new FileWriter(fileLocation, true), ',');
        String[] headers = {"URL", "URL Type"};
        csvWriter.writeNext(headers);
    }

    public void processURL(WebURL webURL){
        String urlType = null;

        String subdomain = webURL.getSubDomain();
        String domain = null;
        if (subdomain!=null && subdomain.length()>1){
            domain = subdomain+"."+webURL.getDomain();
        }
        else{
            domain = webURL.getDomain();
        }

        if(domain.equals(department))
            urlType = "OK";
        else if(domain.equals(school))
            urlType = "USC";
        else
            urlType = "outUSC";

        String[] values = {webURL.getURL(), urlType};
        csvWriter.writeNext(values);
    }

    public void close() throws IOException{
        csvWriter.close();
    }
}
