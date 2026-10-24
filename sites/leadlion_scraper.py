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
# Company ---> LeadLion
# Link ------> https://leadlion.ro/cariere/
#
#
from urllib.parse import urljoin

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from LeadLion scraper.
    '''
    soup = GetStaticSoup("https://leadlion.ro/cariere/")

    job_list = []
    for job in soup.select('article'):

        title_tag = job.select_one('h3 a')
        if not title_tag:
            continue

        link = urljoin('https://leadlion.ro/cariere/', title_tag['href'])
        if 'cariere' in link:

            # get jobs items from response
            job_list.append(Item(
                job_title=title_tag.text.strip(),
                job_link=link,
                company='LeadLion',
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

    company_name = "LeadLion"
    logo_link = "https://leadlion.ro/wp-content/uploads/2020/09/logo-black-2.png.webp"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
