import requests
from lxml import html

CATEGORIES_URL = 'https://itunes.apple.com/us/genre/ios/id36?mt=8'
dict_category_parent = {}
dict_category_url = {}

def get_page_content(url):
    page = requests.get(url)
    return page.text


def get_all_categories():
    #todo handle error case
    page_text = get_page_content(CATEGORIES_URL)
    tree = html.fromstring(page_text)

    for column in ["list column first", "list column", "list column last"]:
        path = '//*[@id="genre-nav"]//ul[@class="%s"]/li' % column

        for element in tree.xpath(path):
            category_url = element.xpath('a/@href')[0]
            category_name = element.xpath('a/text()')[0]
            dict_category_url[category_name] = category_url

            # now check for subcategories
            child = element.xpath('ul[@class="list top-level-subgenres"]')
            if child:
                child_element = child[0]
                for subcategory in child_element.xpath('li/a'):
                    subcategory_name = subcategory.xpath('text()')[0]
                    subcategory_url = subcategory.xpath('@href')[0]
                    dict_category_url[subcategory_name] = subcategory_url
                    # set parent for subcategories
                    dict_category_parent[subcategory_name] = category_name

if __name__=='__main__':
    get_all_categories()
    print dict_category_parent
    print dict_category_url