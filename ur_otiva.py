import requests
from bs4 import BeautifulSoup
import csv



def get_html(url):

	r = requests.get(url)
	return r.text

def get_total_pages(html):
	soup = BeautifulSoup(html, 'lxml')
	pages = soup.find('div', class_="pagination-pages").find_all('a', class_="pagination-page")[-1].get('href')
	total_pages = pages.split('=')[1].split('&')[0]

	return int(total_pages)

def write_csv(data):
  with open('avito.csv', 'a') as f:

	writer  = csv.writer(f)
	writer.writerow( (data['title'],data['price'],data['city'],data['time'],data['img'],data['url']) )


def get_page_data(html):
	soup = BeautifulSoup(html, 'lxml')
	ads = soup.find('div', class_='snippet-list').find_all('div', class_='item_table')
	for ad in ads:

		name = ad.find('div', class_='description').find('h3').text.encode('utf-8').strip().lower()
		if 'htc' in name:

			try:
				title = ad.find('div', class_='description').find('h3').text.encode('utf-8').strip()
			except:
				title = 'none'
			try:
				url = 'https://www.avito.ru' + ad.find('div', class_='description').find('a').get('href')
			except:
				url = ' none '
			try:
				price = ad.find('div', class_='snippet-price-row').find('span', class_='snippet-price').text.encode('utf-8').strip()
			except:
				price = 'none'
			try:
				img = ad.find('div', class_='item-slider-image').find('img', class_='large-picture-img').get('src')
			except:
				img = 'none'
			try:
				city = ad.find('div', class_='item-address-georeferences').find('span', class_='item-address-georeferences-item__content').text.encode('utf-8').strip()
			except:
				city = 'none'
			try:
				time = ad.find('div', class_='snippet-date-row').find('div', class_='snippet-date-info').text.encode('utf-8').strip()
			except:
				time = 'none'

			data = {'title': title,'price': price,'city': city,'time': time,'img': img,'url': url}

			write_csv(data)
		else:
			continue



def main():
	url = 'https://www.avito.ru/rostovskaya_oblast/telefony?bt=1&q=htc'
	base_url = 'https://www.avito.ru/rostovskaya_oblast/telefony?'
	page_part = 'p='
	query_part = '&q=htc'

	total_pages = get_total_pages(get_html(url))

	for i in range(1, total_pages):
		url_gen = base_url + page_part + str(i) + query_part
		html = get_html(url_gen)
		get_page_data(html)



if __name__ == '__main__':
	main()
