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
# Company ---> UpTeam
# Link ------> https://www.upteam.com/careers
#              (redirects to https://www.cloudgeometry.com/careers)
#
#
import requests

from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)

CAREERS_URL = "https://www.cloudgeometry.com/careers"
BASE_URL = "https://www.cloudgeometry.com"


def get_location_data(job_text):
    '''
    ... normalize UpTeam Romania job location.
    '''
    text_lower = job_text.lower()

    if 'cluj-napoca' in text_lower:
        county_data = get_county(location='Cluj')
        return county_data[0] if True in county_data else 'Cluj', 'Cluj-Napoca', 'remote'

    if 'romania' in text_lower and 'remote' in text_lower:
        return '', 'Romania', 'remote'

    if 'remote' in text_lower:
        return '', 'Romania', 'remote'

    return '', 'Romania', 'on-site'


def scraper():
    '''
    ... scrape data from UpTeam scraper.
    '''
    try:
        soup = GetStaticSoup(CAREERS_URL)
    except (requests.exceptions.ConnectTimeout, requests.exceptions.Timeout,
            requests.exceptions.ConnectionError):
        return []

    job_list = []
    for job in soup.find_all('div', class_='w-dyn-item'):
        link_tag = job.find('a', href=True)
        title_tag = job.find('h2') or job.find(class_='semi-20')

        if link_tag is None or title_tag is None:
            continue

        location_tag = job.find(class_='semi-18')
        location_text = location_tag.get_text(' ', strip=True) if location_tag else ''

        county, city, remote = get_location_data(location_text)

        link = link_tag['href']
        job_link = link if link.startswith('http') else BASE_URL + link

        job_list.append(Item(
            job_title=title_tag.get_text(strip=True),
            job_link=job_link,
            company='UpTeam',
            country='Romania',
            county=county,
            city=city,
            remote=remote,
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "UpTeam"
    logo_link = "https://global-uploads.webflow.com/6400e0ba2d1b077f024a81b0/6400edbf3cc188c78f15c3c1_UpTeam_logo.svg"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
