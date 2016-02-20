import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.url.WebURL;
import java.io.IOException;
import java.util.regex.Pattern;
import org.apache.http.HttpStatus;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class SimpleCrawler extends WebCrawler{
    private static final Logger logger = LoggerFactory.getLogger(SimpleCrawler.class);

    public static Pattern pattern = Pattern.compile(".*(\\.(css|js|gif|jpg" + "|png|mp3|mp3|zip|gz))$");

    private URLDownload urlDownload;
    private URLFetch urlFetch;
    private URLDiscovered urlDiscovered;

    public SimpleCrawler() throws IOException{
        urlDownload = new URLDownload();
        urlFetch = new URLFetch();
        urlDiscovered = new URLDiscovered();
    }

    @Override
    public boolean shouldVisit(Page referringPage, WebURL url){
        String href = url.getURL().toLowerCase();

        urlDiscovered.processURL(url);
        return !pattern.matcher(href).matches() && href.startsWith("http://www.arch.usc.edu");

    }

    @Override
    public void visit(Page page){
        String url = page.getWebURL().getURL();

        urlFetch.processURL(url, page.getStatusCode());
        try{
            if(page.getStatusCode() == HttpStatus.SC_OK){
                urlDownload.processPage(page);

            }
        }catch (IOException ioException){
            logger.error("Exception in running crawler" + ioException.toString());
        }
    }

    @Override
    public void onBeforeExit(){
        try{
            urlDiscovered.close();
            urlFetch.close();
            urlDiscovered.close();
        }catch (IOException ioException){
            logger.error("Error while closing the files");
        }
    }
}
