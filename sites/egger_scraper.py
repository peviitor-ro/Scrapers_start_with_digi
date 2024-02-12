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
# Company ---> EGGER
# Link ------> https://careers.egger.com/go/Jobs-in-Romania/8984955/
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
    ... scrape data from EGGER scraper.
    '''
    soup = GetStaticSoup("https://careers.egger.com/go/Jobs-in-Romania/8984955/")

    job_list = []
    for job in soup.find_all('tr', attrs={'class': 'data-row'}):

        # one time for link and title
        title_link = job.find('a', attrs={'class': 'jobTitle-link'})

        # get location
        location = job.find('span', attrs={'class': 'jobLocation'}).text.strip().split(',')[0]

        # get jobs items from response
        job_list.append(Item(
            job_title=title_link.text,
            job_link='https://careers.egger.com' + title_link['href'],
            company='EGGER',
            country='Romania',
            county=get_county(location),
            city=location,
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "EGGER"
    logo_link = "https://rmkcdn.successfactors.com/24f99312/dac140b7-bf0d-474e-b2c7-7.jpg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
