import requests
from bs4 import BeautifulSoup
import shutil

count = 1
while count <= 3:

    url = "http://baskino.club/new/page/" + str(count)
    page = requests.get(url).text

    soup = BeautifulSoup(page)
    divs = soup.findAll("div", {'class': 'shortpost'})

    def content():

        for div in divs:
            title = div.find('div', {'class': "posttitle"})
            link_text = title.find('a').text
            img = div.find('div', {'class': "postcover"})
            img_src = img.find('img').get('src')
            response = requests.get(img_src, stream=True)
            with open(link_text.replace('/img', '') + '.jpg', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            print link_text
        return

    count +=1

    print content()
