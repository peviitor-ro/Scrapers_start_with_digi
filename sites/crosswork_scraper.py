#
#
#
# Company - crosswork
# Link -> https://crosswork.sincron.biz/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_data_from_crosswork():
    """
    ... get data from crosswork with one requests.
    """

    response = requests.get(url='https://crosswork.sincron.biz/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='row')

    lst_with_data = []
    for dt in soup_data:

        job_data = dt.find('h3', class_='h3-list-job-title')

        if job_data:
            title = job_data.find('a').text
            link = job_data.find('a')['href']
            city = dt.find('p', class_='job-info').find('span').text

            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "crosswork",
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


company_name = 'crosswork'
data_list = get_data_from_crosswork()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('crosswork',
                  'https://crosswork.sincron.biz/images/routes/5023/logo-crosswork.png'))
