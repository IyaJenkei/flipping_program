import requests
import bs4 as bs
from ebaysdk.finding import Connection as Finding
from statistics import mean

import ebaykey

region = "semo" #want to create a function that grabs your region.
BASE_URL = "https://" + region + ".craigslist.org/search/sss"
craigslist_soup = bs.BeautifulSoup(requests.get(BASE_URL).text, 'lxml')

APP_ID = ebaykey.ebay_key()

item = input("what item do you want? ")


def create_craigslist_dict(soup):

    title_list = []
    price_list = []

    for row in soup.find_all('p', class_='result-info'):
        for title in row.find_all('a', class_='result-title'):
            title_list.append(title.string)

    for row in soup.find_all('p', class_='result-info'):
        for price in row.find_all('span', class_='result-price'):
            price_list.append(int((price.string.lstrip("$"))))

    craigslist_dict = dict(zip(title_list, price_list))

    craigslist_dict = {k: v for k, v in craigslist_dict.items() if int(v) < 999}

    return craigslist_dict

def search_ebay(item):

    api = Finding(appid=APP_ID, config_file=None)
    response = api.execute('findItemsAdvanced', {'keywords': item})

    return response.dict()

def average_ebay_price(item):

    price_list = []

    for result in search_ebay(item)['searchResult']['item']:

        price_list.append(float(result['sellingStatus']['currentPrice']['value']))

    return(mean(price_list))


def find_deals(dict,item):

    avg_price = average_ebay_price(item)

    for item1, price in cl_dict.items():
        if int(price) < int((avg_price * .5)):
            print(item, price, avg_price)


cl_dict = create_craigslist_dict(craigslist_soup)

find_deals(cl_dict, item)
