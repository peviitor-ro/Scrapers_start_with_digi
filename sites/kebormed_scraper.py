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
# Company ---> KeborMed
# Link ------> https://kebormed.com/careers/index.html
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
    ... scrape data from KeborMed scraper.
    '''
    soup = GetStaticSoup("https://kebormed.com/careers/index.html")

    job_list = []
    for job in soup.select('#careers a'):

        # get jobs items from response
        job_list.append(Item(
            job_title=job.select_one('div.text').text,
            job_link=job['href'],
            company='KeborMed',
            country='Romania',
            county='',
            city='',
            remote='remote',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "KeborMed"
    logo_link = "https://kebormed.com/images/logo.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
