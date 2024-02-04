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
# Company ---> Connect44
# Link ------> https://www.connect44.com/careers/jobs\?country\=3\&search\=
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
    ... scrape data from Connect44 scraper.
    '''
    soup = GetStaticSoup("https://www.connect44.com/careers/jobs?country=3&search=")

    job_list = []
    # walrus - best option
    if len((data_soup := soup.find_all('div', attrs={'class': 'col-md-6'}))) > 0:
    
        for job in data_soup:
            location = job.find('span', attrs={'class': 'me-3 d-flex align-items-center'}).text.strip().split(',')[-1].strip()
            if location.lower() == "bucharest":
                location = "Bucuresti"

            # get jobs items from response
            job_list.append(Item(
                job_title=job.find('div', attrs={'class': 'mb-4 d-flex align-items-center'}).text.strip(),
                job_link=job.find('a', attrs={'class': 'stretched-link'})['href'].strip(),
                company='Connect44',
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

    company_name = "Connect44"
    logo_link = "https://www.totaljobs.com/CompanyLogos/32ec644942c1486e89eb54318d6eed92.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
