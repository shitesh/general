import au.com.bytecode.opencsv.CSVWriter;

import java.io.FileWriter;
import java.io.IOException;

public class URLError {

    private CSVWriter csvWriter;
    private final String fileLocation = "output/skipped.csv";

    public URLError() throws IOException {
        csvWriter = new CSVWriter(new FileWriter(fileLocation, true), ',');
    }

    public void processURL(String[] missed){
        csvWriter.writeNext(missed);

    }

    public void close() throws IOException{
        csvWriter.close();
    }
}
