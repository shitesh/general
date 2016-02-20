/* class to keep track of all the urls that were fetched after passing the discovery phase. This will save the url in a file in format
        URL, HTTPSTatusCode
*/


import au.com.bytecode.opencsv.CSVWriter;

import java.io.FileWriter;
import java.io.IOException;

public class URLFetch{
    private CSVWriter csvWriter;
    private final String fileLocation = "output/fetch.csv";

    public URLFetch() throws IOException{
        csvWriter = new CSVWriter(new FileWriter(fileLocation), ',');
    }

    public void processURL(String url, Integer statusCode){
        String status = String.valueOf(statusCode);
        String[] values = {url, status};
        csvWriter.writeNext(values);

    }

    public void close() throws IOException{
        csvWriter.close();
    }
}
