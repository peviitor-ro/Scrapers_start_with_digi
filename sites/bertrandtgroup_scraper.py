#
#
#
# Make new Scraper for bertrandtgroup --->
# Link to this Company ---> https://bertrandtgroup.onlyfy.jobs/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def return_soup(url: str):
    """
    ... return soup object from link.
    """
    response = requests.get(url=url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    return soup


def get_soup_data(url: str) -> int:
    """
    Return total nums of jobs from Bertrandtgroup
    """


def collect_data_from_site() -> list:
    """
    This func() return all data from site.
    """

    # collect data!
    lst_with_data = []

    # facem request la pagina principala si extragem csrf_token
    soup = return_soup(url=f'https://bertrandtgroup.onlyfy.jobs')
    csrf_token = soup.find('meta', attrs={'name': 'csrf-token'})['content']

    # setam un header nou cu csrf_token
    session = requests.Session()

    params = {
        "candidate_center_filter[country]": "RO",
        "candidate_center_filter[hasCityCluster]": 0,
        "csrf_token": csrf_token
    }

    # facem un post request cu parametrii de mai sus
    first_call = session.post(url='https://bertrandtgroup.onlyfy.jobs/candidate/job/filter?search=', data=params, headers=DEFAULT_HEADERS)

    # facem un get request pentru a lua toate joburile
    last_call = session.get(url='https://bertrandtgroup.onlyfy.jobs/candidate/job/ajax_list?display_length=200&page=1&sort=matching&sort_dir=DESC&_=1684168027359', headers=DEFAULT_HEADERS)

    soup = BeautifulSoup(last_call.text, 'lxml')

    jobs = soup.find_all('div', class_='row')

    for job in jobs:
        link = job.find('div', class_='inner').find('a')['href']
        title = job.find('div', class_='inner').find('a').text
        city = job.find_all('div', class_='inner')[1].text.strip()

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  'https://bertrandtgroup.onlyfy.jobs' + link,
                "company": "bertrandtgroup",
                "country": "Romania",
                "city": city
            })

    return lst_with_data


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'bertrandtgroup'
data_list = collect_data_from_site()
scrape_and_update_peviitor(company_name, data_list)

# update Logo
print(update_logo('bertrandtgroup', 'https://content.prescreen.io/company/logo/2zflb91e9rc4s8gskgco4g84gss0kgw.jpg'))
