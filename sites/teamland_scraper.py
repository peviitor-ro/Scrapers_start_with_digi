#
#
# Config for Dynamic Get Method -> For JSON format.
#
# Company ---> Teamland
# Link ------> https://www.teamland.ro/index.php#joburi_table
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
from bs4 import BeautifulSoup

from __utils import (
    GetRequestJson,
    get_county,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from Teamland scraper.
    '''
    json_data = GetRequestJson("https://www.teamland.ro/j.php?_=1686681054574")
    jobs_data = json_data.get('data') or []

    job_list = []
    for job in jobs_data:
        job_id = job[0]
        job_title_tag = BeautifulSoup(job[1], 'lxml').find('span')
        job_location_tag = BeautifulSoup(job[2], 'lxml').find('span')

        if job_title_tag is None or job_location_tag is None:
            continue

        job_title = job_title_tag.text.strip()
        job_location = job_location_tag.text.strip()
        first_city = job_location.split(',')[0].strip()
        location_finish = get_county(location=first_city)

        job_list.append(Item(
            job_title=job_title,
            job_link=f'https://www.teamland.ro/apply.php?id={job_id}#content',
            company='Teamland',
            country='Romania',
            county=location_finish[0] if True in location_finish else '',
            city=job_location,
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Teamland"
    logo_link = "https://www.teamland.ro/img/logo.png"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
