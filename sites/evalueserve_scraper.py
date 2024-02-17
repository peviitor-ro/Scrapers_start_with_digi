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
# Company ---> Evalueserve
# Link ------> https://www.evalueserve.com/jobs/
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
    ... scrape data from Evalueserve scraper.
    '''
    soup = GetStaticSoup("https://www.evalueserve.com/jobs/")

    job_list = []
    for job in soup.select('div[class$="Romania"]'):

        # get location
        location = job.select_one('div.db-location-country > h6').text.split(',')

        # get jobs items from response
        job_list.append(Item(
            job_title=job.select_one('div.db-job-title > h4').text,
            job_link=job.select_one('div.db-job-link > a')['href'],
            company='Evalueserve',
            country='Romania',
            county=location[1],
            city=location[0],
            remote='remote',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Evalueserve"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
