import ConfigParser
import os
import requests
from bs4 import BeautifulSoup



CONFIG_LOCATION = "config.cfg"

def read_config(config_file_location):
    config = ConfigParser.ConfigParser()
    config.read(config_file_location)
    url = config.get("DOWNLOADER_CONFIG", "URL")
    output_dir = config.get("DOWNLOADER_CONFIG", "OUTPUT_DIR")
    return url, output_dir

def save_image(image_url, output_directory):
    #TODO : put some better logic for image names
    image_name = image_url.split("/")[-1]
    output_path = os.path.join(output_directory, image_name)

    file = open(output_path, "wb")
    image_response = requests.get(image_url, stream=True)
    for chunk in image_response.iter_content():
        file.write(chunk)

    file.close()

def process_url(url, output_directory):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    for image in soup.find_all("img"):
        if image.attrs.has_key("src") and image["src"].startswith("http"):
            image_url = image["src"]
            save_image(image_url, output_directory)

if __name__=='__main__':
    url, output_directory_location = read_config(CONFIG_LOCATION)
    if not os.path.exists(output_directory_location):
        os.makedirs(output_directory_location)
    process_url(url, output_directory_location)
