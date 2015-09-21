import ConfigParser
import csv
import os
import requests
import string
from lxml import html
from datetime import  datetime

CONFIG_LOCATION = "config.cfg"
dict_config = {}
csv_writer = None
file_object = None


def read_config(config_file_location):
    config = ConfigParser.ConfigParser()
    config.read(config_file_location)
    dict_config.update(config._sections['DOWNLOADER_CONFIG'])

def save_state(reset=False):
    config= ConfigParser.ConfigParser()
    config.read(CONFIG_LOCATION)

    if reset:
        temp_dict = {'last_category_scraped_name': '', 'last_category_scraped_url': '', 'last_page_scraped': '',
                     'last_alphabet_scraped': ''
        }
        dict_config.update(temp_dict)

    for key, value in dict_config.iteritems():
        config.set('DOWNLOADER_CONFIG', key, value)

    with open(CONFIG_LOCATION, 'wb') as configfile:
        config.write(configfile)

def get_writer_object():
    global csv_writer, file_object
    if csv_writer:
        return csv_writer
    else:
        file_name = 'APP_DETAILS.csv'
        file_name = os.path.join(dict_config['output_dir'], file_name)
        file_object = open(file_name, 'w')
        csv_writer = csv.writer(file_object, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['APP ID', 'APP NAME', 'CATEGORY', 'SUBCATEGORY', 'APP URL'])
        return csv_writer

def close_file():
    global file_object
    if file_object:
        file_object.close()

def get_page_tree(url):
    page = requests.get(url)
    return html.fromstring(page.text)

def get_apps(category, subcategory, category_url, alphabet, page_num=1):
    prev_app_name_list = []
    count = 0
    dict_app_url = {}
    csv_writer = get_writer_object()

    while True:
        current_app_list = []
        url = '%s&letter=%s&page=%s' % (category_url, alphabet, page_num)
        tree = get_page_tree(url)
        for element in tree.xpath('//*[@id="selectedcontent"]//li/a'):
            app_name = element.xpath('text()')[0].encode('utf8')
            app_url = element.xpath('@href')[0]
            current_app_list.append(app_name)
            if app_name in prev_app_name_list:
                continue
            dict_app_url[app_name] = app_url
            count += 1

        if set(current_app_list) == set(prev_app_name_list):
            break

        if count > 3000:
            for app_name, app_url in dict_app_url.iteritems():
                app_id = app_url.split('/')[-1].split('?')[0][2:]
                csv_writer.writerow([app_id, app_name, category, subcategory, app_url])
            dict_config['last_category_scraped_name'] = subcategory if subcategory else category
            dict_config['last_category_scraped_url'] = category_url
            dict_config['last_page_scraped'] = page_num
            dict_config['last_alphabet_scraped'] = alphabet
            dict_app_url = {}
            count = 0

        prev_app_name_list = current_app_list
        page_num += 1

    for app_name, app_url in dict_app_url.iteritems():
        app_id = app_url.split('/')[-1].split('?')[0][2:]
        csv_writer.writerow([app_id, app_name, category, subcategory, app_url])
    save_state()

def parse_app_list(category_url_list, dict_category_parent):
    category_count = 0
    start_page_num = None
    start_alphabet = None

    # create a list of all alphabets and append * - url corresponding to # in istore
    all_valid_suburls = [alphabet for alphabet in string.ascii_uppercase]
    all_valid_suburls.append('*')

    if dict_config['last_category_scraped_name']:
        last_index = category_url_list.index((dict_config['last_category_scraped_name'], dict_config['last_category_scraped_url']))
        category_url_list = category_url_list[last_index:]

        start_page_num = int(dict_config['last_page_scraped']) + 1
        start_alphabet = dict_config['last_alphabet_scraped']

    for category, category_url in category_url_list:
        # find if parent category is present
        subcategory = None

        if category_url in dict_category_parent:
            subcategory = category
            category = dict_category_parent[category_url]

        print 'starting with category: %s url:%s subcategory: %s' %(category, category_url, subcategory)
        print datetime.now()
        for alphabet in all_valid_suburls:
            if start_alphabet:
                if alphabet == start_alphabet:
                    get_apps(category, subcategory, category_url, alphabet, start_page_num)
                    start_alphabet = None
                continue
            get_apps(category, subcategory, category_url, alphabet)
        # one category completely processed, close the file
        print datetime.now()
        category_count += 1

    close_file()
    save_state(True)

def get_all_categories():
    dict_category_parent = {}
    category_url_list = []
    tree = get_page_tree(dict_config['url'])

    for column in ["list column first", "list column", "list column last"]:
        path = '//*[@id="genre-nav"]//ul[@class="%s"]/li' % column

        for element in tree.xpath(path):
            category_url = element.xpath('a/@href')[0]
            category_name = element.xpath('a/text()')[0]

            # now check for subcategories
            child = element.xpath('ul[@class="list top-level-subgenres"]')
            if child:
                child_element = child[0]
                for subcategory in child_element.xpath('li/a'):
                    subcategory_name = subcategory.xpath('text()')[0]
                    subcategory_url = subcategory.xpath('@href')[0]

                    category_url_list.append((subcategory_name, subcategory_url))
                    dict_category_parent[subcategory_url] = category_name
            category_url_list.append((category_name, category_url))

    return category_url_list, dict_category_parent

if __name__=='__main__':
    read_config(CONFIG_LOCATION)
    category_url_list, dict_category_parent = get_all_categories()
    parse_app_list(category_url_list, dict_category_parent)
