#
#
#
# Company - Verifone
# Link - https://www.verifone.com/en/careers/search?locations%5B%5D=8729&keyword=
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_data_from_verifone():
    """
    ... get data from verifone with one requests.
    """

    response = requests.get(url='https://www.verifone.com/en/global/careers/jobs?title=&departments=All&locations=686',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('tr')

    lst_with_data = []
    for dt in soup_data:
        link = dt.find('a')
        title = dt.find('a')
        location = dt.find('td', attrs={'class': 'views-field views-field-field-offices'})

        if link is not None:
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title.text.strip(),
                "job_link": link['href'].strip(),
                "company": "verifone",
                "country": "Romania",
                "city": location.text.strip()
                })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'verifone'
data_list = get_data_from_verifone()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('verifone',
                  'https://datasym.co.uk/wp-content/uploads/2017/09/verifone-logo-300x120.png'
                  ))
