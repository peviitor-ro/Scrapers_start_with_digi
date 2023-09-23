#
#
#
# Company -> monefy
# link -> https://monefy.ro/careers/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_html_data():
    '''
    ... get data with one requests.
    '''

    response = requests.get(url='https://monefy.ro/careers/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('article')

    list_duplicate = []
    lst_with_data = []
    for dt in soup_data:
        data = dt.find('h3', class_='entry-title').find('a')

        link = data['href']
        title = data.text

        if title not in list_duplicate:
            list_duplicate.append(title)

            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "monefy",
                "country": "Romania",
                "city": "Romania"
                })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'monefy'
data_list = get_html_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('monefy',
                  'https://monefy.ro/wp-content/uploads/2021/02/Logo.png'
                  ))
