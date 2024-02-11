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
# Company ---> CanamGroup
# Link ------> https://www.canam.com/en/job-opportunities/?country%5B%5D=romania&search=
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
    ... scrape data from CanamGroup scraper.
    '''
    soup = GetStaticSoup("https://www.canam.com/en/job-opportunities/?country%5B%5D=romania&search=")

    job_list = []
    for job in soup.find_all('a', attrs={'class': 'c-card-job'}):
        location = job.find('div', attrs={'class': 'c-btn c-btn--ghost c-btn--tag u-pointer-events-none'}).text.strip()

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find('div', attrs={'class': 'c-card-job__title u-heading-600'}).find('span').text,
            job_link=job.get('href'),
            company='CanamGroup',
            country='Romania',
            county=get_county(location),
            city=location,
            remote=get_job_type(location),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "CanamGroup"
    logo_link = "https://www.canam.com/wp-content/themes/canam/dist/img/logo-canam.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
