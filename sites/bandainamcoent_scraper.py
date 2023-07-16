#
#
#
#
# Company -> bandainamcoent
# Link ----> https://www.bandainamcoent.ro/ro/careers/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_site() -> list[dict]:
    '''
    ... collect all data from site with one requests.
    '''

    response = requests.get(url='https://www.bandainamcoent.ro/ro/careers/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('p', attrs={'class': 'career_job_links has-text-align-center has-black-color has-text-color'})

    lst_with_data = []
    for sd in soup_data:
        link = 'https://www.bandainamcoent.ro' + sd.find('a')['href'].replace('.', 'careers')
        title = sd.find('a').text

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "bandainamcoent",
                "country": "Romania",
                "city": "Romania"
            })

    return lst_with_data


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'bandainamcoent'
data_list = collect_data_from_site()
scrape_and_update_peviitor(company_name, data_list)

# update Logo
print(update_logo('bandainamcoent',
                  'https://www.bandainamcoent.ro/wp-content/themes/namco/img/logo_small.jpg'))
