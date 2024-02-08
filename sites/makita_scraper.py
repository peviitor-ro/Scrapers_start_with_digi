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
# Company ---> makita
# Link ------> https://makitajobs.ro/locuri-de-munca/
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
    ... scrape data from makita scraper.
    '''
    soup = GetStaticSoup("https://makitajobs.ro/locuri-de-munca/")

    job_list = []
    for job in soup.find_all('div', attrs={'class': 'box-right'}):
        link = "https://makitajobs.ro" + job.find('div', attrs={'class': 'content-button'}).find('a')['href']

        # search location
        location = GetStaticSoup(link).find_all('div', attrs={'class': 'text'})[-1].find('p').text.split()[-1].strip()

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find('div', attrs={'class': 'content-title'}).text,
            job_link=link,
            company='makita',
            country='România',
            county=get_county(location),
            city='All',
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "makita"
    logo_link = "https://www.makita.ro/data/pam/public/makita_logo3.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
