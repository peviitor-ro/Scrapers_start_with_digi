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
# Company ---> Serrala
# Link ------> https://careers.serrala.com/search/\?searchby\=distance\&createNewAlert\=false\&q\=\&geolocation\=\&d\=10\&lat\=\&lon\=\&optionsFacetsDD_dept\=\&optionsFacetsDD_location\=\&optionsFacetsDD_country\=RO
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
    ... scrape data from serrala scraper.
    '''
    soup = GetStaticSoup("https://careers.serrala.com/search/?searchby=distance&createNewAlert=false&q=&geolocation=&d=10&lat=&lon=&optionsFacetsDD_dept=&optionsFacetsDD_location=&optionsFacetsDD_country=RO")

    job_list = []
    for job in soup.find_all('tr', class_='data-row'):

        link = job.find('a')
        location = job.find('span', class_='jobLocation').text.strip().split(',')[0]
        if location.lower() == 'bucharest':
            location = 'Bucuresti'

        location_finish = get_county(location=location)

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find('a').text.strip(),
            job_link="https://careers.serrala.com" + link['href'],
            company='serrala',
            country='Romania',
            county=location_finish[0] if True in location_finish else None,
            city='all' if location.lower() == location_finish[0].lower()\
                        and True in location_finish and 'bucuresti' != location.lower()\
                            else location,
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "serrala"
    logo_link = r"https://cookie-cdn.cookiepro.com/logos/c260fbd9-3298-48e4-8478-41e8a0cb0ab7/24f7e702-f5ef-4966-a29c-cd2ea3fab97b/de6ed974-29cf-418d-ad05-21dd545142de/serrala-vector-logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()