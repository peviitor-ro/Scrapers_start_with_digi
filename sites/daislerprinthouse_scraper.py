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
# Company ---> DaislerPrintHouse
# Link ------> https://www.daisler.ro/despre-noi/cariere
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
    ... scrape data from DaislerPrintHouse scraper.
    '''
    soup = GetStaticSoup("https://www.daisler.ro/despre-noi/cariere")

    job_list = []
    
    # get data with walrus
    if len(data_from_soup := soup.select('div.item')) > 0:

        for job in data_from_soup:

            # get jobs items from response
            job_list.append(Item(
                job_title=job.select_one('div.item-details > h2').text,
                job_link=job.select_one('a')['href'],
                company='DaislerPrintHouse',
                country='Romania',
                county='Cluj',
                city='Cluj-Napoca',
                remote='on-site',
            ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "DaislerPrintHouse"
    logo_link = "https://www.daisler.ro/skin/frontend/daisler/default/images/logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
