#
#
# Your custom scraper here ---> Last level!
#
# Company ---> BertrandtGroup
# Link ------> https://bertrandt.jobs.hr.cloud.sap/search/
#
#
# Aici va invit sa va creati propriile metode de scraping cu Python,
# ... folosind:
# -> requests
# -> BeautifulSoup
# -> requests_html etc.
#
import html
import re
import time
import urllib.parse

import requests
from bs4 import BeautifulSoup

from __utils import Item, get_county, UpdateAPI
from __utils import DEFAULT_HEADERS


SITEMAP_URL = 'https://bertrandt.jobs.hr.cloud.sap/sitemap.xml'
ARCHIVED_SITEMAP_URL = (
    'https://web.archive.org/web/20261011153820id_/'
    'https://bertrandt.jobs.hr.cloud.sap/sitemap.xml'
)

CITY_ALIASES = {
    'bukarest': 'Bucuresti',
    'bucharest': 'Bucuresti',
    'bucuresti': 'Bucuresti',
    'sibiu': 'Sibiu',
    'hermannstadt': 'Sibiu',
    'cluj': 'Cluj-Napoca',
    'cluj-napoca': 'Cluj-Napoca',
    'klausenburg': 'Cluj-Napoca',
    'timisoara': 'Timisoara',
    'temeswar': 'Timisoara',
    'brasov': 'Brasov',
    'kronstadt': 'Brasov',
    'iasi': 'Iasi',
    'constanta': 'Constanta',
    'craiova': 'Craiova',
    'oradea': 'Oradea',
    'arad': 'Arad',
    'pitesti': 'Pitesti',
    'mioveni': 'Mioveni',
    'bacau': 'Bacau',
    'galati': 'Galati',
    'ploiesti': 'Ploiesti',
    'suceava': 'Suceava',
    'targu-mures': 'Targu Mures',
}


def return_soup(url: str):
    """
    ... return soup object from link.
    """
    response = requests.get(url=url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    return soup


def get_sitemap_urls(session: requests.Session):
    """
    ... get job urls from the live sitemap, falling back to the archived one
    when the career site is unavailable.
    """
    for sitemap_url in (SITEMAP_URL, ARCHIVED_SITEMAP_URL):
        for attempt in range(3):
            try:
                response = session.get(sitemap_url, headers=DEFAULT_HEADERS, timeout=30)
            except requests.RequestException:
                break

            if response.status_code == 200:
                urls = [
                    html.unescape(url)
                    for url in re.findall(r'<loc>(.*?)</loc>', response.text, re.S)
                ]
                if urls:
                    return urls
                break

            if response.status_code != 429:
                break

            time.sleep(5 * (attempt + 1))

    return []


def get_fallback_title(job_path: str):
    """
    ... build a readable title from a job path.
    """
    title = job_path

    for alias in sorted(CITY_ALIASES, key=len, reverse=True):
        if title.lower().startswith(f'{alias}-'):
            title = title[len(alias) + 1:]
            break

    title = re.sub(r'-\d{4,}$', '', title)
    return re.sub(r'[\s_-]+', ' ', title).strip()


def get_city_from_path(job_path: str):
    """
    ... map a sitemap job path to its Romanian city, if it is a Romanian job.
    """
    normalized_path = urllib.parse.unquote(job_path).lower()

    for alias in sorted(CITY_ALIASES, key=len, reverse=True):
        if normalized_path == alias or normalized_path.startswith(f'{alias}-'):
            return CITY_ALIASES[alias]

    return None


def get_job_title(soup: BeautifulSoup, fallback_title: str):
    """
    ... get the job title from the job page.
    """
    title_meta = soup.find('meta', attrs={'property': 'og:title'})
    if title_meta and title_meta.get('content'):
        return html.unescape(title_meta['content']).strip()

    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.get_text(strip=True)
        if ' Job Details |' in title:
            return title.split(' Job Details |', 1)[0].strip()

    return fallback_title


def scraper():
    """
    This func() return all data from site.
    """

    session = requests.Session()

    sitemap_urls = get_sitemap_urls(session)

    # collect data!
    job_list = []
    for job_url in sitemap_urls:
        if '/job/' not in job_url:
            continue

        job_path = urllib.parse.unquote(job_url.split('/job/', 1)[1].split('/', 1)[0])
        location = get_city_from_path(job_path)
        if not location:
            continue

        fallback_title = get_fallback_title(job_path)
        title = fallback_title

        try:
            response = session.get(job_url, headers=DEFAULT_HEADERS, timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                title = get_job_title(soup, fallback_title)
        except requests.RequestException:
            pass

        if location.lower() in ['bucharest', 'bukarest']:
            location = 'Bucuresti'

        job_type = 'on-site'
        if 'remote' in title.lower():
            job_type = 'remote'

        location_finish = get_county(location=location)

        job_list.append(Item(
            job_title=title,
            job_link=job_url,
            company='BertrandtGroup',
            country='Romania',
            county=location_finish[0] if True in location_finish else None,
            city='all' if location.lower() == location_finish[0].lower()\
                    and True in location_finish and 'bucuresti' != location.lower()\
                        else location,
            remote=job_type,
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
