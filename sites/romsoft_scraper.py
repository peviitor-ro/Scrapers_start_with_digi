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
# Company ---> RomSoft
# Link ------> https://www.rms.ro/careers/
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
    ... scrape data from RomSoft scraper.
    '''
    soup = GetStaticSoup("https://www.rms.ro/careers/")

    job_list = []
    for job in soup.select('div.awsm-job-listing-item.awsm-list-item'):

        # get jobs items from response
        job_list.append(Item(
            job_title=job.select_one('h2.awsm-job-post-title').text.strip(),
            job_link=job.select_one('a.awsm-job-more')['href'],
            company='RomSoft',
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

    company_name = "RomSoft"
    logo_link = "https://www.rms.ro/wp-content/uploads/2021/09/logo.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
