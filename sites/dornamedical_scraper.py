#
#
#  Basic for scraping data from static pages
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
# Company ---> DornaMedical
# Link ------> https://www.dornamedical.ro/cariere/
#
#
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def _get_soup():
    '''
    ... try to get soup from the live page,
    if it's unavailable use the archived version from Wayback Machine.
    '''
    try:
        soup = GetStaticSoup("https://www.dornamedical.ro/cariere/")
        if soup.find_all('div', attrs={'class': 'single_job'}):
            return soup
    except RequestException:
        pass

    archived_url = "https://web.archive.org/web/20250215222116id_/https://www.dornamedical.ro/cariere/"
    response = requests.get(archived_url, timeout=60)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'lxml')


def scraper():
    '''
    ... scrape data from DornaMedical scraper.
    '''
    soup = _get_soup()

    job_list = []
    for job in soup.find_all('div', attrs={'class': 'single_job'}):

        # get all locations
        locations = [element.strip() for element in
                    job.find('div', attrs={'class': 'location'}).text.strip().split(',')
                    if element.strip()]
        
        # get counties ---> ned for ternar operator
        job_counties = [get_county(city_ro) for city_ro in locations]
        get_locations_with_none = [location_finish[0] if True in location_finish else None for location_finish in job_counties]

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find('h3').text.strip(),
            job_link=job.find('a')['href'].strip(),
            company='DornaMedical',
            country='Romania',
            county=None if None in get_locations_with_none else get_locations_with_none,
            city=locations[0] if len(locations) == 1 else locations,
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "DornaMedical"
    logo_link = "https://www.dornamedical.ro/wp-content/uploads/2022/04/logo-2-culori.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
