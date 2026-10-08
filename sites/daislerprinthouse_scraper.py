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
# Link ------> https://www.daisler.ro/cariere
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

SOURCE_LINK = "https://www.daisler.ro/cariere"


def scraper():
    '''
    ... scrape data from DaislerPrintHouse scraper.
    '''
    soup = GetStaticSoup(SOURCE_LINK)

    job_list = []

    # get data with walrus
    if len(data_from_soup := soup.select('div.cariere-container div.card')) > 0:

        for job in data_from_soup:

            job_title_elem = job.select_one('div.card-title')
            if not job_title_elem:
                continue

            apply_link_elem = job.select_one('a[href]')
            job_link = apply_link_elem['href'] if apply_link_elem and apply_link_elem['href'].startswith('http') else SOURCE_LINK

            job_list.append(Item(
                job_title=job_title_elem.text.strip(),
                job_link=job_link,
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
