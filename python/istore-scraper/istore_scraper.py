""" I-STORE SCRAPPER

    This script scrapes the appstore categories page and using the links present there, gets info of all the apps
    present in the appstore.

    Key points about the appstore:
    1.  The category page is alphabetically indexed, each alphabet page having the url structure:
        https://itunes.apple.com/us/genre/ios-<category-name>/<category-id>?mt=8&letter=<alphabet>&page=<page-number>
    2.  If the requested page number is greater than the maximum page number of an alphabet, it always returns the same
        page.

    Functionality:
    1.  All necessary info is maintained in the config file. It also contains fields for last category, alphabet and page
        number scraped. If present, the next run will start from there only.
    1.  Scrapes the category page to get category list. Structure is maintained in such a way that all the child
        categories are scraped before its parent.
    2.  Using category urls and key point(1) above, gets 5 details for all the apps - appid, app name, category,
        subcategory and app url.
    3.  Dumps the data in a single csv file with appropriate headers.

"""

import ConfigParser
import csv
import logging
import os
import requests
import string
import smtplib
import ssl
from functools import wraps
from lxml import html
from email.mime.text import MIMEText

CONFIG_LOCATION = "config.cfg"
dict_config = {}
csv_writer = None
file_object = None
logger = None

def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar

def read_config(config_file_location):
    """ Updates the config dictionary

    This function reads the config file and updates the config dictionary to be used in other functions.
    """
    config = ConfigParser.ConfigParser()
    config.read(config_file_location)
    dict_config.update(config._sections['DOWNLOADER_CONFIG'])

def set_logging(log_file_location):
    """Sets the logging info

    This function sets the logging parameters and logging format. Log file location is read from config dictionary.
    """
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(log_file_location)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

def set_writer_object(output_directory, file_name):
    """Creates output file object and csv writer    """

    global csv_writer, file_object

    file_name = os.path.join(output_directory, file_name)
    if dict_config['last_category_scraped_name']:
        file_object = open(file_name, 'a')
    else:
        file_object = open(file_name, 'w')

    csv_writer = csv.writer(file_object, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    if not dict_config['last_category_scraped_name']:
        csv_writer.writerow(['APP ID', 'APP NAME', 'CATEGORY', 'SUBCATEGORY', 'APP URL'])

def send_mail(exception):
    MAIL_HOST = dict_config['smtp_host']
    MAIL_FROM = dict_config['mail_from']
    PASSWORD = dict_config['mail_from_password']
    MAIL_TO = dict_config['mail_to'].split(',')

    subject = 'Exception occcured while parsing app store'

    text = 'The following exception occured while parsing the app store: \n\n'
    text = '%s %s' %(text, exception)

    msg = MIMEText(text)
    msg['To'] = ','. join([str(x) for x in MAIL_TO])
    msg['From'] = MAIL_FROM
    msg['Subject'] = subject
    try:
        smtpObj = smtplib.SMTP(MAIL_HOST)
        smtpObj.starttls()
        smtpObj.login(MAIL_FROM, PASSWORD)
        smtpObj.sendmail(MAIL_FROM, MAIL_TO, msg.as_string())
        smtpObj.close()
    except Exception, e:
       logger.exception(e)

def save_state(reset=False):
    """ Updates the config and closes the output file

    Saves the final state at which the program ends. If True is passed as the parameter, it means that the program has
    successfully ended and so it sets the record of last scraped entities to null. Else it records the last
    scraped entities so that re-run can start from that point.
    """
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

    if file_object:
        file_object.close()

def get_page_tree(url):
    """ Parses the given url and returns its content    """

    page = requests.get(url)
    return html.fromstring(page.text)

def get_apps(category, subcategory, category_url, alphabet, page_num=1):
    """Get details of all the apps for a given category and alphabet

    Writes to the file only when 3000 apps has been scraped and updates the config dictionary once write is complete
    """
    prev_app_name_list = []
    count = 0
    dict_app_url = {}

    logger.info('Scraping apps with starting alphabet: %s' % alphabet)
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

            # update the config dictionary, dont save state now as it will be unnecessary writes
            dict_config['last_category_scraped_name'] = subcategory if subcategory else category
            dict_config['last_category_scraped_url'] = category_url
            dict_config['last_page_scraped'] = page_num
            dict_config['last_alphabet_scraped'] = alphabet

            # write complete, reset the app dictionary and count
            dict_app_url = {}
            count = 0

        prev_app_name_list = current_app_list
        page_num += 1

    # handle the case when 3000 apps were not reached in final run of the loop
    for app_name, app_url in dict_app_url.iteritems():
        app_id = app_url.split('/')[-1].split('?')[0][2:]
        csv_writer.writerow([app_id, app_name, category, subcategory, app_url])

    dict_config['last_category_scraped_name'] = subcategory if subcategory else category
    dict_config['last_category_scraped_url'] = category_url
    dict_config['last_page_scraped'] = page_num
    dict_config['last_alphabet_scraped'] = alphabet

def parse_app_list(category_url_list, dict_category_parent):
    """Parses all the categories and get app details

    Calls get_apps() internally
    """
    start_page_num = None
    start_alphabet = None

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

        logger.info('parsing subcategory: %s of category: %s with url: %s.' %(subcategory, category, category_url))
        for alphabet in all_valid_suburls:
            if start_alphabet:
                if alphabet == start_alphabet:
                    get_apps(category, subcategory, category_url, alphabet, start_page_num)
                    start_alphabet = None
                continue
            get_apps(category, subcategory, category_url, alphabet)

    save_state(True)

def get_all_categories(url):
    """Returns all categories list and parent dictionary present in app store

    Parses the url given in config file, creates a list of (category name, category url) and a dictionary of mapping app
    urls to parent category names.
    """
    logger.info('Scraping Main Categories page')
    dict_category_parent = {}
    category_url_list = []
    tree = get_page_tree(url)

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

    logger.info('Main categories page scraping complete')
    return category_url_list, dict_category_parent


if __name__=='__main__':
    read_config(CONFIG_LOCATION)
    set_logging(dict_config['log_file_location'])
    ssl.wrap_socket = sslwrap(ssl.wrap_socket)
    try:
        set_writer_object(dict_config['output_dir'], dict_config['file_name'])

        category_url_list, dict_category_parent = get_all_categories(dict_config['url'])
        parse_app_list(category_url_list, dict_category_parent)

        save_state(True)
    except Exception, err:
        logger.info('Exception occured in the script.')
        logger.exception(err)
        send_mail(err)
        save_state()
