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
# Company ---> Fabric
# Link ------> https://blog-qa.fabricdata.com/corporate/careers
#
#
from __utils import (
    GetStaticSoup,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from Fabric scraper.
    '''
    soup = GetStaticSoup("https://blog-qa.fabricdata.com/corporate/careers")

    job_list = []
    no_jobs_text = soup.find('h3')
    if no_jobs_text and 'not hiring' in no_jobs_text.get_text(' ', strip=True).lower():
        return job_list

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Fabric"
    logo_link = "https://mma.prnewswire.com/media/1701193/Fabric2_Logo.jpg?p=twitter"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
