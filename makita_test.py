#
#
import requests
from bs4 import BeautifulSoup

# job url
url = "https://makitajobs.ro/locuri-de-munca/"

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
}

response = requests.get(url=url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')

boxes = soup.select('div.box-right')

for job in boxes:
    title = job.select_one('div.content-title').text
    #
    link = job.select_one('div.content-button a').get('href')
    if link:
        link = 'https://makitajobs.ro' + link

    print(link, title, sep=" <---> ")
