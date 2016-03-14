import edu.uci.ics.crawler4j.crawler.CrawlConfig;
import edu.uci.ics.crawler4j.crawler.CrawlController;
import edu.uci.ics.crawler4j.fetcher.PageFetcher;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtConfig;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtServer;

public class Controller {

    public static URLDownload urlDownload;
    public static URLDiscovered urlDiscovered;
    public static URLFetch urlFetch;
    public static URLError urlError;

    public static void main(String[] args) throws Exception{
        urlDiscovered = new URLDiscovered();
        urlDownload = new URLDownload();
        urlError = new URLError();
        urlFetch = new URLFetch();

        String storageFolder = "output/stats";
        String startUrl = "http://arch.usc.edu/";
        int numberOfCrawlers = 7;

        CrawlConfig crawlConfig = new CrawlConfig();

        crawlConfig.setCrawlStorageFolder(storageFolder);
        crawlConfig.setMaxDepthOfCrawling(5);
        crawlConfig.setMaxPagesToFetch(5000);

        //crawlConfig.setPolitenessDelay(1000);
        crawlConfig.setMaxDownloadSize(100000000);
        crawlConfig.setIncludeBinaryContentInCrawling(true);

        PageFetcher pageFetcher = new PageFetcher(crawlConfig);
        RobotstxtConfig robotstxtConfig = new RobotstxtConfig();
        RobotstxtServer robotstxtServer = new RobotstxtServer(robotstxtConfig, pageFetcher);
        CrawlController crawlController = new CrawlController(crawlConfig, pageFetcher, robotstxtServer);

        crawlController.addSeed(startUrl);

        try{
            crawlController.start(SimpleCrawler.class, numberOfCrawlers);
        }catch(Exception e){
            System.out.println(e.getMessage());
        }

        urlFetch.close();
        urlDiscovered.close();
        urlDownload.close();
        urlError.close();
    }
}
