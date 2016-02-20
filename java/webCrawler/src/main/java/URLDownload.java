import au.com.bytecode.opencsv.CSVWriter;
import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.parser.BinaryParseData;
import edu.uci.ics.crawler4j.parser.HtmlParseData;
import edu.uci.ics.crawler4j.url.WebURL;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Set;

/**
 * Created by shitesh on 2/19/16.
 */


/* class to keep track of all the urls that were actually downloaded. This will save multiple data points:
        1. URL, size of File, number of outlinks, content type - visit.csv
        2. URL, outlinks - pagerankdata.csv
        3. dowloaded file html
*/

/* TODO - how to save pdf, doc and docx files?
   TODO - duplicate links??
*/

public class URLDownload {
    private CSVWriter visitWriter;
    private CSVWriter pageRankWriter;
    private final String visitFile = "output/visit.csv";
    private final String pageRankFile = "output/pagerankdata.csv";

    public final String storageFolder = "output/data/";

    public URLDownload() throws IOException{
        visitWriter = new CSVWriter(new FileWriter(visitFile));
        pageRankWriter = new CSVWriter(new FileWriter(pageRankFile));
    }


    public void savePage(Page page) throws IOException{
        String url = page.getWebURL().getURL();

        String filePath = storageFolder + url;
        FileOutputStream fileOutputStream = new FileOutputStream(filePath);
        fileOutputStream.write(page.getContentData());
        fileOutputStream.close();

    }

    public void processPage(Page page) throws IOException{
        savePage(page);

        //TODO - check this
        String  size = String.valueOf(page.getContentData().length);
        String url = page.getWebURL().getURL();
        String contentType = page.getContentType();
        Set<WebURL> outGoingLinks = null;

        if(page.getParseData() instanceof BinaryParseData){
            BinaryParseData binaryParseData = (BinaryParseData) page.getParseData();
            outGoingLinks = binaryParseData.getOutgoingUrls();
        }

        else if(page.getParseData() instanceof HtmlParseData){
            HtmlParseData htmlParseData = (HtmlParseData) page.getParseData();
            outGoingLinks = htmlParseData.getOutgoingUrls();
        }
        String numberOfOutgoingLinks = String.valueOf(outGoingLinks.size());

        // populate the pagerank.csv
        String[] pageRankValues = new String[outGoingLinks.size()+1];
        pageRankValues[0] = url;
        Integer index = 1;
        for(WebURL webURL: outGoingLinks){
            pageRankValues[index] = webURL.getURL();
        }
        pageRankWriter.writeNext(pageRankValues);


        // populate the visit.csv
        String[] visitValues = {url, size, numberOfOutgoingLinks, contentType};
        visitWriter.writeNext(visitValues);

    }

    public void close() throws IOException{
        visitWriter.close();
        pageRankWriter.close();
    }
}
