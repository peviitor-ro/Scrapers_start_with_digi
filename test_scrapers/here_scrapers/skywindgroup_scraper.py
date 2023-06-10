#
#
#
# Company -> skywindgroup
# Link json -> https://careers.skywindgroup.com/careers/careers.json
# Link to site -> https://careers.skywindgroup.com/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_data_from_json() -> list:
    """
    ... return data from web with one requests.
    """

    response = requests.get(url='https://careers.skywindgroup.com/careers/careers.json',
                            headers=DEFAULT_HEADERS).json()

    titles = BeautifulSoup(response['content'], 'lxml')

    hash_data = []
    for dt in titles.find_all('li'):

        # store data
        title = dt.find('a').text
        link = dt.find('a')['href']
        city = dt.find('span', class_='BambooHR-ATS-Location').text

        # add data to hash data
        hash_data.append(f"{title}-{link}-{city}")

    return list(set(hash_data))


def decrypt_data_from_hash() -> tuple:
    """
    ... here decrypt data from hash.
    """

    new_data = get_data_from_json()

    lst_decrypt = []
    for dt in new_data:
        data = dt.split('-')

        # extract data
        title = data[0]
        link = "https:" + data[1]
        city = data[2].split()[-1]

        # sort data for Roumania
        cities = ['bucuresti', 'bucharest', 'iasi', 'cluj', 'cluj-napoca',
                  'constanta', 'timisoara', 'brasov',
                  'craiova', 'galati', 'oradea']
        if city.lower() in cities:
            lst_decrypt.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "skywindgroup",
                "country": "Romania",
                "city": city
                })

    return lst_decrypt, len(lst_decrypt)


data_list = decrypt_data_from_hash()
