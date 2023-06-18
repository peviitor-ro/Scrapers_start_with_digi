#
#
#
# Company -> updivision
# Link -> https://updivision.com/careers?variable=tech
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_data_with_from_updivision() -> list:
    """
    ... return data from site with one requests.
    Request to html.
    """

    response = requests.get(url='https://updivision.com/careers?variable=tech',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='container-jobs')

    lst_with_data = []
    for dt in soup_data:
        title = dt.find('a').text

        # makek url from title
        link = title.lower().replace('.', '').replace('+ ', '').replace('(', '').replace(')', '').replace('& ', '')

        # append all data to list
        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  'https://updivision.com/careers/' + '-'.join(list(link.split())),
                "company": "updivision",
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


company_name = 'updivision'
data_list = get_data_with_from_updivision()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('updivision',
                  'https://api.arcadier.com/assets/admin/uploads/partner/logo_UPD_6378125.jpg'
                  ))
