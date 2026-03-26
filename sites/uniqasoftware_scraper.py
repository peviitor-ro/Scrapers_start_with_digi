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
# Company ---> UNIQA Software Services
# Link ------> https://www.uniqasoftware.ro/join-uss/
#
#
from __utils import (
    GetStaticSoup,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from UNIQA Software Services scraper.
    '''
    soup = GetStaticSoup("https://www.uniqasoftware.ro/join-uss/")

    join_link = soup.find('a', href='https://uniqasoftware.mingle.ro/en/apply')
    if join_link is None:
        return []

    return []


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "UNIQA Software Services"
    logo_link = "https://www.uniqasoftware.ro/wp-content/uploads/2021/04/120x60.jpeg"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
