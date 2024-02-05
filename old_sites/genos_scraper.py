#
#
#
# New Company - Genos
# Link to scrape -> https://www.genosdanmark.eu/vacancies
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_genos():
    """
    Collect data from Genos, from HTML.
    """

    response = requests.get('https://www.genosdanmark.eu/vacancies',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    #
    soup_data = soup.find('div', class_='col-sm-12 col-md-8 col-lg-9').find_all('div', class_='row')[0]

    lst_with_data = []
    for dt in soup_data.find_all('div', class_='product-item'):
        link = dt.find('h4', class_='product-item__title').find('a')['href']
        title = dt.find('h4', class_='product-item__title').find('a').text

        lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link":  'https://www.genosdanmark.eu/' + link,
                    "company": "genos",
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


company_name = 'genos'
data_list = collect_data_from_genos()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('genos',
                  'https://www.genosdanmark.eu/uploads/images/logo-dark_27_12.png'
                  ))
