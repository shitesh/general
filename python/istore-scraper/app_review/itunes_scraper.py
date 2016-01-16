import requests
from lxml import html
import ConfigParser
import logging
import os
import json
import csv
from email.mime.text import MIMEText
import smtplib


dict_config = {}
CONFIG_FILE_LOCATION = 'config.cfg'
logger = None
file_object = None


def read_config(config_file_location):
    global dict_config

    config = ConfigParser.ConfigParser()
    config.read(config_file_location)
    dict_config.update(config._sections['DOWNLOADER_CONFIG'])


def set_file_object(output_directory, file_name):
    file_path = os.path.join(output_directory, file_name)
    file_object = open(file_path, 'w')
    return file_object

def set_logging(log_file_location):
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(log_file_location)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def save_config(reset):
    global dict_config
    config= ConfigParser.ConfigParser()
    config.read(CONFIG_FILE_LOCATION)

    if reset:
        temp_dict = {'last_id_scraped': ''}
        dict_config.update(temp_dict)

    for key, value in dict_config.iteritems():
        config.set('DOWNLOADER_CONFIG', key, value)

    with open(CONFIG_FILE_LOCATION, 'wb') as configfile:
        config.write(configfile)


def send_mail(forbidden_list):
    MAIL_HOST = dict_config['smtp_host']
    MAIL_FROM = dict_config['mail_from']
    PASSWORD = dict_config['mail_from_password']
    MAIL_TO = dict_config['mail_to'].split(',')

    subject = 'Got 403 while parsing app store'

    text = 'Received 10 continuous 403 response from the app store. App details are as follows: \n\n'
    for x in forbidden_list:
        text += '%s, %s, %s\n' % (x[0], x[1], x[2])

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


def get_app_list(input_file_location):
    global dict_config
    dict_app_id = {}
    app_list = []
    last_id_scraped = dict_config['last_id_scraped']

    file = open(input_file_location, 'r')
    reader = csv.reader(file, delimiter=',')
    #skip the header
    next(reader, None)

    for row in reader:
        if last_id_scraped:
            if row[0].strip() == last_id_scraped:
                last_id_scraped = None
            continue

        if not dict_app_id.has_key(row[0].strip()):
            dict_app_id[row[0].strip()] = 1
            app_list.append(row[0].strip())
    return app_list


def get_page_tree(url):
    headers = {'User-Agent':'iTunes/9.2 (Macintosh; U; PPC Mac OS X 10.6)', "X-Apple-Store-Front": "143441-1" }
    page = requests.get(url, headers=headers)
    if page.status_code == 403:
        return True, None

    return False, html.fromstring(page.content)


def get_reviews_for_app(app_id):
    global logger

    comment_list = []
    page_num = 0
    url = "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewContentsUserReviews?id=%s&pageNumber=%d&sortOrdering=4&onlyLatestVersion=false&type=Purple+Software" % (app_id, page_num)

    is_forbidden, tree = get_page_tree(url)
    if is_forbidden:
        return True, None

    page_num_string = tree.xpath("document/view/scrollview/vboxview/view/matrixview/vboxview[1]/vboxview/hboxview[2]/textview/setfontstyle/b/text()")
    if not page_num_string:
        logger.error('No reviews found for %s' %(app_id))
        return False, None

    total_num_page = page_num_string[0].strip().split(' ')[-1]

    for page_num in xrange(0, int(total_num_page)):
        url = "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewContentsUserReviews?id=%s&pageNumber=%d&sortOrdering=4&onlyLatestVersion=false&type=Purple+Software" % (app_id, page_num)
        is_forbidden, tree = get_page_tree(url)

        if is_forbidden:
            return True, None


        for comment_index in xrange(1,26):
            current_comment, username, version, date = None, None, None , None
            xpath = "document/view/scrollview/vboxview/view/matrixview/vboxview[1]/vboxview/vboxview[%s]/textview/setfontstyle/text()" %(comment_index)
            comment = tree.xpath(xpath)
            if comment:
                current_comment = comment[0].replace('\n', '').strip()

            username_xpath = "document/view/scrollview/vboxview/view/matrixview/vboxview[1]/vboxview/vboxview[%s]/hboxview[2]/textview/setfontstyle/gotourl/b/text()" % (comment_index)
            username = tree.xpath(username_xpath)
            if username:
                username = username[0].replace('\n', '').strip()

            details_xpath = 'document/view/scrollview/vboxview/view/matrixview/vboxview[1]/vboxview/vboxview[%s]/hboxview[2]/textview/setfontstyle/text()' %(comment_index)
            details = tree.xpath(details_xpath)
            if details and details[1]:
                detail_list = details[1].replace('\n', '').strip().split('-')
                version = detail_list[1].strip() if detail_list[1] else None
                date = detail_list[2].strip() if detail_list[2] else None

            if current_comment:
                dict_temp = {'comment': current_comment, 'username': username, 'version': version, 'date': date}
                comment_list.append(dict_temp)

    return False, comment_list

if __name__ == '__main__':
    read_config(CONFIG_FILE_LOCATION)
    set_logging(dict_config['log_file_location'])
    app_list = get_app_list(dict_config['input_file_location'])
    missed_file = open(dict_config['missed_ids'], 'a')

    count_403 = 0
    forbidden_list = []
    for app_id in app_list:
        try:
            is_forbidden, comment_list = get_reviews_for_app(app_id)
            if is_forbidden:
                missed_file.write('%s\n' % app_id)
                logger.error("Forbidden from the app store: %s" % app_id)
                count_403 += 1
                forbidden_list.append(app_id)
                if count_403 >= 10:
                    save_config(False)
                    send_mail(forbidden_list)
                continue

            if not comment_list:
                missed_file.write('%s\n' % app_id)
                continue
            count_403 = 0
            forbidden_list = []

            dict_app_id = {}
            dict_config['last_id_scraped'] = app_id
            dict_app_id['app_id'] = app_id
            dict_app_id['comments'] = comment_list
            app_json = json.dumps(dict_app_id)
            file_object = set_file_object(dict_config['output_dir'], '%s_review.json' % app_id)
            file_object.write('%s\n' % app_json)
            file_object.close()
            save_config(False)
        except Exception, err:
            logger.error("Could not find data for : %s" % app_id)
            logger.error(err)
            continue
