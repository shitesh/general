import au.com.bytecode.opencsv.CSVWriter;
import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.parser.BinaryParseData;
import edu.uci.ics.crawler4j.parser.HtmlParseData;
import edu.uci.ics.crawler4j.url.WebURL;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Set;
import java.util.regex.Pattern;

/* class to keep track of all the urls that were actually downloaded. This will save multiple data points:
        1. URL, size of File, number of outlinks, content type - visit.csv
        2. URL, outlinks - pagerankdata.csv
        3. dowloaded file html
*/

public class URLDownload {
    private CSVWriter visitWriter;
    private CSVWriter pageRankWriter;
    private final String visitFile = "output/visit.csv";
    private final String pageRankFile = "output/pagerankdata.csv";

    public final String storageFolder = "output/data/";


    private final static String pattern = ".*(\\.(html|htm|doc|pdf|docx))$";
    private final static Pattern FILTERS = Pattern.compile(pattern);



    public URLDownload() throws IOException{
        visitWriter = new CSVWriter(new FileWriter(visitFile, true), ',');
        pageRankWriter = new CSVWriter(new FileWriter(pageRankFile, true), ',');

        String[] visitHeaders = {"URL", "Size", "No of outlinks", "Content-type"};
        visitWriter.writeNext(visitHeaders);
    }


    public void savePage(Page page) throws IOException{
        String url = page.getWebURL().getURL().replaceAll("/$","");
        url = url.replaceAll("/", "--");

        String filePath = storageFolder + url;
        FileOutputStream fileOutputStream = new FileOutputStream(filePath, false);
        fileOutputStream.write(page.getContentData());
        fileOutputStream.close();

    }


    public static Boolean isValidUrl(Page page){
        String url = page.getWebURL().getURL();
        String contentType = page.getContentType();

        if(contentType.contains("text/html")
                || contentType.contains("application/msword")
                || contentType.contains("application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                || contentType.contains("application/pdf")){
            return true;
        }
        else if (FILTERS.matcher(url).matches()) {
            return true;
        }

        String[] values = {"isValidUrl filter", url, contentType};
        Controller.urlError.processURL(values);
        return false;
    }

    public void processPage(Page page) throws IOException{
        if(!isValidUrl(page)){
            return;
        }

        savePage(page);
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
            index++;
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
