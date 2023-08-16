#
#
#
#
# Company -> Bunge
# Link ----> https://jobs.bunge.com/search/?createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_country=
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_data_from_bunge() -> list[dict]:
    '''
    ... collect data from bunge with one request.
    Site return a html with data.
    '''

    response = requests.get(url='https://jobs.bunge.com/search/?createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_country=',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('tr', class_='data-row')

    lst_with_data = []
    for sd in soup_data:
        link = sd.find('a', class_='jobTitle-link')['href']
        title = sd.find('a', class_='jobTitle-link').text
        city = sd.find('span', class_='jobLocation').text.strip().split(',')[0]

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": 'https://jobs.bunge.com' + link,
                "company": "Bunge",
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


company_name = 'Bunge'
data_list = get_data_from_bunge()
scrape_and_update_peviitor(company_name, data_list)

# update Logo
print(update_logo('Bunge',
                  'https://rmkcdn.successfactors.com/c8d09bed/298fb332-da77-4747-9f6b-9.svg'))
