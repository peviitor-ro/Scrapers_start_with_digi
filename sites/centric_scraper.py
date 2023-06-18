#
#
#
# Company - centric
# Link -> https://careers.centric.eu/ro/open-positions/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import re 
import json

#Am folosit regex deoarece joburile sunt afisate prin javascript
pattern = re.compile(r'window.FILTER_BAR_INITIAL = (.*);')

def get_data_from_centric():
    """
    ... get data from centric with one requests.
    """

    response = requests.get(url='https://careers.centric.eu/ro/open-positions/',
                            headers=DEFAULT_HEADERS)
    
    data = json.loads(pattern.search(response.text).group(1)).get('results')

    soup = BeautifulSoup(data[0], 'lxml')

    soup_data = soup.find_all('div', class_='card')

    lst_with_data = []
    for dt in soup_data:

        if soup_data:
            title = dt.find('div',class_='card__title').text
            link = dt.find('a')['href']
            city = dt.find('div', class_='tag-list').find_all('span', class_="tag__span")[1].text

            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "centric",
                "country": "Romania",
                "city": city
            })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'centric'
data_list = get_data_from_centric()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('centric',
                  'https://www.oribi.nl/cache/centric.2994/centric-s1920x1080.png'))
