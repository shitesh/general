import edu.uci.ics.crawler4j.crawler.CrawlConfig;
import edu.uci.ics.crawler4j.crawler.CrawlController;
import edu.uci.ics.crawler4j.fetcher.PageFetcher;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtConfig;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtServer;

/**
 * Created by shitesh on 2/18/16.
 */
public class Controller {

    public static void main(String[] args) throws Exception{
        String storageFolder = "output/data";
        String startUrl = "https://arch.usc.edu/";
        int numberOfCrawlers = 4;

        CrawlConfig crawlConfig = new CrawlConfig();
        crawlConfig.setCrawlStorageFolder(storageFolder);


        //TODO - why the fuck are we doing this??
        PageFetcher pageFetcher = new PageFetcher(crawlConfig);
        RobotstxtConfig robotstxtConfig = new RobotstxtConfig();
        RobotstxtServer robotstxtServer = new RobotstxtServer(robotstxtConfig, pageFetcher);
        CrawlController crawlController = new CrawlController(crawlConfig, pageFetcher, robotstxtServer);

        crawlController.addSeed(startUrl);

        crawlController.start(SimpleCrawler.class, numberOfCrawlers);

    }
}
