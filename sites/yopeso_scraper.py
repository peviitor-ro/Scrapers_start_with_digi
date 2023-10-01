#
#
#
# Company -> yopeso
# Link -> https://careers.yopeso.com/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_data_from_yopeso() -> list:
    """
    ... return a list with data from yopeso with one requests.
    """

    response = requests.get(url='https://careers.yopeso.com/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='uzptka-1 ddeuCH')

    lst_with_data = []
    for dt in soup_data:
        title = dt.find('a', class_='sc-6exb5d-1 harIFI').text
        link = dt.find('a', class_='s03za1-0 krhJaE')['href']
        city = dt.find('span', class_='custom-css-style-job-location-city').text

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  "https://careers.yopeso.com/" + link,
            "company": "yopeso",
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


company_name = 'yopeso'
data_list = get_data_from_yopeso()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('yopeso',
                  'https://www.yopeso.com/wp-content/uploads/2022/05/logo-Yopeso-150x78.png'
                  ))
