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
# Company ---> Updivision
# Link ------> https://updivision.com/careers
#
#
import json

from __utils import (
    get_county,
    GetStaticSoup,
    Item,
    UpdateAPI,
)


DEFAULT_ROMANIA_CITY = 'Bucuresti'
DEFAULT_ROMANIA_COUNTY = get_county(location=DEFAULT_ROMANIA_CITY)[0]


def get_jobs_data():
    '''
    ... extract jobs from structured data on Updivision careers page.
    '''
    soup = GetStaticSoup("https://updivision.com/careers")

    for script in soup.find_all('script', attrs={'type': 'application/ld+json'}):
        script_text = script.string or script.get_text()
        if 'JobPosting' not in script_text:
            continue

        return json.loads(script_text).get('itemListElement', [])

    return []


def scraper():
    '''
    ... scrape data from Updivision scraper.
    '''
    job_list = []
    for item in get_jobs_data():
        job = item.get('item') or {}
        job_title = job.get('title')
        job_link = job.get('url')
        location = ((job.get('jobLocation') or {}).get('address') or {}).get('addressLocality', 'Romania')
        country = ((job.get('jobLocation') or {}).get('address') or {}).get('addressCountry', 'Romania')

        if not job_title or not job_link:
            continue

        if str(country).lower() != 'romania':
            continue

        remote = 'remote' if str(location).lower() == 'remote' else 'on-site'
        city = DEFAULT_ROMANIA_CITY if remote == 'remote' else location

        job_list.append(Item(
            job_title=job_title,
            job_link=job_link,
            company='Updivision',
            country='Romania',
            county=DEFAULT_ROMANIA_COUNTY if remote == 'remote' else '',
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

    company_name = "Updivision"
    logo_link = "https://api.arcadier.com/assets/admin/uploads/partner/logo_UPD_6378125.jpg"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
