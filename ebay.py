import requests
from bs4 import BeautifulSoup
import csv
import shutil


URL = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=bike&_sacat=0'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}

FILE = 'ebay.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='pagination__item')
    if pagination:
        return(pagination[-1].get_text())
    else:
        return 1

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='s-item__wrapper clearfix')

    products = []
    for item in items:

        products.append({
            'title': item.find('h3', class_='s-item__title').get_text(),
            'sub_title': item.find('div', class_='s-item__subtitle').get_text(),
            'price': item.find('span', class_='s-item__price').get_text(),
            'location': item.find('span', class_='s-item__location s-item__itemLocation').get_text(),
            'link': item.find('a', class_='s-item__link').get('href'),
            'img_link': item.find('img', class_='s-item__image-img').get('src')

        })
    return products


def save_file(items, path):
    with open(path, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'SubTitle', 'Price', 'Location', 'Link','Img Link'])
        for item in items:
            writer.writerow([
                            item['title'].encode('utf-8'),
                            item['sub_title'].encode('utf-8'),
                            item['price'],
                            item['location'],
                            item['link'],
                            item['img_link']
                            ])


def parse():
    URL = raw_input("put URL: ")
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        products = []
        pages_count = get_pages_count(html.text)
        for page in range(1, 5):
            print("Scraping page %(page)s" % {"page": page, "pages_count": pages_count})
            html = get_html(URL, params={'page': page})
            products.extend(get_content(html.text))
        save_file(products, FILE)
        print len(products), " total products"
        
    else:
        print('Error')

parse()
