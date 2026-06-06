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
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from Neptun scraper.
    '''
    soup = GetStaticSoup("https://www.neptun-gears.ro/cariere/")

    job_list = []
    for job in soup.select_one('.fusion-text-2 ul').select('li'):
        job_list.append(Item(
            job_title=job.text.strip(),
            job_link='https://www.neptun-gears.ro/cariere/',
            company='Neptun',
            country='Romania',
            county='Prahova',
            city='Campina',
            remote='on-site',
        ).to_dict())

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
