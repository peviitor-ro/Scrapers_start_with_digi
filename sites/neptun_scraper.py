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
# Company ---> Neptun
# Link ------> https://www.neptun-gears.ro/ro/cariere/
#
#
import requests
from bs4 import BeautifulSoup
from __utils import (
    GetStaticSoup,
    DEFAULT_HEADERS,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

CAREERS_URL = "https://www.neptun-gears.ro/cariere/"
EJOBS_URL = "https://www.ejobs.ro/company/s-c-neptun-s-a/73778"


def _get_jobs_from_careers_page():
    '''
    ... get jobs from the company careers page.
    '''
    soup = GetStaticSoup(CAREERS_URL)

    job_list = []
    jobs_container = soup.select_one('.fusion-text-2 ul')
    if jobs_container:
        for job in jobs_container.select('li'):
            job_list.append(Item(
                job_title=job.text.strip(),
                job_link=CAREERS_URL,
                company='Neptun',
                country='Romania',
                county='Prahova',
                city='Campina',
                remote='on-site',
            ).to_dict())

    return job_list


def _get_jobs_from_ejobs():
    '''
    ... fallback to the company page on eJobs when the careers site is down.
    '''
    response = requests.get(EJOBS_URL, headers=DEFAULT_HEADERS, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    job_list = []
    seen_links = set()
    for link in soup.select('a[href*="/user/locuri-de-munca/"]'):
        title = link.get_text(' ', strip=True)
        href = link.get('href', '')

        if not title or href in seen_links:
            continue

        seen_links.add(href)
        job_list.append(Item(
            job_title=title,
            job_link=f"https://www.ejobs.ro{href}",
            company='Neptun',
            country='Romania',
            county='Prahova',
            city='Campina',
            remote='on-site',
        ).to_dict())

    return job_list


def scraper():
    '''
    ... scrape data from Neptun scraper.
    '''
    try:
        job_list = _get_jobs_from_careers_page()
    except requests.RequestException:
        job_list = []

    if not job_list:
        try:
            job_list = _get_jobs_from_ejobs()
        except (requests.RequestException, ValueError):
            job_list = []

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Neptun"
    logo_link = "https://www.neptun-gears.ro/images/logo.jpg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
