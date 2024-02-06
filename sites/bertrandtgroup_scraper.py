#
#
# Your custom scraper here ---> Last level!
#
# Company ---> BertrandtGroup
# Link ------> https://bertrandtgroup.onlyfy.jobs/
#
#
# Aici va invit sa va creati propriile metode de scraping cu Python,
# ... folosind:
# -> requests
# -> BeautifulSoup
# -> requests_html etc.
#
from __utils import Item, get_county, UpdateAPI
from __utils import DEFAULT_HEADERS
import requests
from bs4 import BeautifulSoup
# from requests_html import HTMLSession


def return_soup(url: str):
    """
    ... return soup object from link.
    """
    response = requests.get(url=url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    return soup


def scraper():
    """
    This func() return all data from site.
    """

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

    # collect data!
    job_list = []
    for job in jobs:
        location = job.find_all('div', class_='inner')[1].text.strip()

        # if location == Bucharest
        if location.lower() in ['bucharest',]:
            location = 'Bucuresti'

        job_list.append(Item(
            job_title=job.find('div', class_='inner').find('a').text,
            job_link='https://bertrandtgroup.onlyfy.jobs' + job.find('div', class_='inner').find('a')['href'],
            company='BertrandtGroup',
            country='Romania',
            county=get_county(location),
            city=location,
            remote='remote',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "BertrandtGroup"
    logo_link = "https://content.prescreen.io/company/logo/2zflb91e9rc4s8gskgco4g84gss0kgw.jpg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
