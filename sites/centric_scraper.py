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
            title = dt.find('div', class_='card__title').text
            link = dt.find('a')['href']
            city = dt.find('div', class_='tag-list').find_all('span', class_="tag__span")[1].text

            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "Centric",
                "country": "Romania",
                "city": city
            })

    return lst_with_data, len(lst_with_data)


print(get_data_from_centric())
