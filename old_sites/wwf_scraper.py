#
#
#
#
# Company -> WWF
# Link ----> https://wwf.ro/despre-wwf/wwf-romania/cariere/
#
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_data_from_WWF() -> list[dict]:
    '''
    ... this func return a list with jobs after get requests.
    '''

    response = requests.get(url='https://wwf.ro/despre-wwf/wwf-romania/cariere/', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', attrs={'class': 'elementor-image-box-content'})

    lst_with_data = []
    for sd in soup_data:
        title = sd.find('a').text.strip()
        link = sd.find('a')['href']

        # check for partial link
        if 'https://wwf.ro' not in link:
            link = "https://wwf.ro" + link

        # check if link is for job
        if 'wwfeu' in link:
            continue

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "WWF",
            "country": "Romania",
            "city": "Bucuresti",
            })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'WWF'
data_list = get_data_from_WWF()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('WWF',
                  'https://cdn.wwf.ro/uploads/2021/04/13154419/wwf-logo-250x281-1.jpg'
                  ))
