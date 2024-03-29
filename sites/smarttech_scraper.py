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
# Company ---> Smarttech
# Link ------> https://www.smarttech247.com/careers/
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
    ... scrape data from Smarttech scraper.
    '''
    soup = GetStaticSoup("https://www.smarttech247.com/careers/")

    job_list = []
    for job in soup.select('div.numbercard'):
        
        # select job title, because location are stored here
        if (title_job := job.select_one('p.maintitle').text) and 'bucharest' in title_job.lower():

            # get jobs items from response
            job_list.append(Item(
                job_title=title_job,
                job_link=job.select_one('a')['href'],
                company='Smarttech',
                country='Romania',
                county='Bucuresti',
                city='Bucuresti',
                remote='on-site',
            ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Smarttech"
    logo_link = "https://pbs.twimg.com/profile_images/1437799338852470792/LapKP2Hx_400x400.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
