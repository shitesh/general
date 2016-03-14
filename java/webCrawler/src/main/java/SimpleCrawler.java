import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.url.WebURL;
import java.io.IOException;
import java.util.regex.Pattern;
import org.apache.http.HttpStatus;
import org.apache.log4j.BasicConfigurator;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SimpleCrawler extends WebCrawler{


    private static Logger logger = LoggerFactory.getLogger(SimpleCrawler.class);

    private final String departmentName = "arch.usc.edu";

    public SimpleCrawler(){
        BasicConfigurator.configure();
    }

    @Override
    public boolean shouldVisit(Page referringPage, WebURL url){
        String href = url.getURL().toLowerCase();
        Controller.urlDiscovered.processURL(url);

        String subdomain = url.getSubDomain();
        String domain = null;
        if (subdomain!=null){
            domain = subdomain+"."+url.getDomain();
        }
        else{
            domain = url.getDomain();
        }

        if(!domain.equals(departmentName)){
            String[] values = {"Should visit method filter", url.getURL(), domain};
            Controller.urlError.processURL(values);
            return false;
        }
        else{
            return true;
        }
        //return domain.equals(departmentName);
    }

    @Override
    public void visit(Page page){
        try{
            if(page.getStatusCode() == HttpStatus.SC_OK){
                Controller.urlDownload.processPage(page);

            }
        }catch (IOException ioException){
            System.out.println(ioException.getMessage());
            logger.error("Exception in running crawler" + ioException.toString());
        }
    }

    @Override
    protected void handlePageStatusCode(WebURL webUrl, int statusCode, String statusDescription) {
        Controller.urlFetch.processURL(webUrl.getURL(),statusCode);
    }

}
