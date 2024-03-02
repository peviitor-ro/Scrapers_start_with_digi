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
# Company ---> NINEDOTS
# Link ------> https://ninedots.io/jobs/
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
    ... scrape data from NINEDOTS scraper.
    '''
    soup = GetStaticSoup("https://ninedots.io/jobs/")

    job_list = []
    for job in soup.select('a.job-card'):
        
        location = [element.text.lower() for element in job.select('p')]
        if 'remote' in str(location) and 'europe' in str(location):

            # get jobs items from response
            job_list.append(Item(
                job_title=location[-1].title(),
                job_link=f'https://ninedots.io{job["href"]}',
                company='NINEDOTS',
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

    company_name = "NINEDOTS"
    logo_link = "https://www.executionlabs.com/wp-content/uploads/2016/02/nine-dots-logo-2.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
