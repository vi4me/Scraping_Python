import requests
from bs4 import BeautifulSoup
import csv
import shutil

# URL = 'https://auto.ria.com/newauto/marka-acura/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='proposition')

    cars = []
    for item in items:
        uah_price = item.find('span', class_='grey size13')
        if uah_price:
            uah_price = uah_price.get_text()
        else:
            uah_price = "Don't have price"
        cars.append({
            'title': item.find('h3', class_='proposition_name').get_text(strip=True),
            'name': item.find('div', class_='proposition_equip size13 mt-5').find('a').get_text(),
            'link': HOST + item.find('h3', class_='proposition_name').find_next('a').get('href'),
            'usd_price': item.find('span', class_='green').get_text(),
            'uah_price': (uah_price),
            'description': item.find('div', class_='proposition_information').get_text(),
            'city': item.find('div', class_='proposition_region grey size13').find('strong').get_text(),
            'img_link': item.find('picture').find('img').get('src')

        })
    return cars


def save_file(items, path):
    with open(path, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['Model', 'Name', 'Link', 'Price $', 'Price UAH', 'Description', 'City', 'Img Link'])
        for item in items:
            writer.writerow([item['title'].encode('utf-8'),
                            item['name'].encode('utf-8'),
                            item['link'],
                            item['usd_price'].encode('utf-8'),
                            item['uah_price'].encode('utf-8'),
                            item['description'].encode('utf-8'),
                            item['city'].encode('utf-8'),
                            item['img_link']])


def parse():
    URL = raw_input("put URL: ")
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count):
            print("Scraping page %(page)s out of %(pages_count)x..." % {"page": page, "pages_count": pages_count})
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)
        print len(cars), " total cars"
    else:
        print('Error')

parse()
