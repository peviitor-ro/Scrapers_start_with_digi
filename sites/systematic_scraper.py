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
# Company ---> Systematic
# Link ------> https://jobs.systematic.com/search/\?createNewAlert\=false\&q\=\&locationsearch\=\&optionsFacetsDD_country\=RO
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
    ... scrape data from Systematic scraper.
    '''
    soup: GetStaticSoup = GetStaticSoup("https://jobs.systematic.com/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_country=RO")

    jobs_num: int = int(soup.select_one('span.paginationLabel').text.split()[-1])

    job_list: list = list()
    #
    start_row_page: int = 0
    while start_row_page < jobs_num:
        #
        soup_jobs: GetStaticSoup = GetStaticSoup(url=f'https://jobs.systematic.com/search/?q=&sortColumn=referencedate&sortDirection=desc&optionsFacetsDD_country=RO&startrow={str(start_row_page)}')

        for job in soup_jobs.select('tr.data-row'):
            if (location := job.select_one('span.jobLocation').text.strip().split(',')[0]) and location.lower() == 'bucharest':
                location = 'Bucuresti'

            location_finish = get_county(location=location)

            # get jobs items from response
            job_list.append(Item(
                job_title=job.select_one('a.jobTitle-link').text,
                job_link=f"https://jobs.systematic.com{job.select_one('a.jobTitle-link').get('href')}",
                company='Systematic',
                country='Romania',
                county=location_finish[0] if True in location_finish else None,
                city='all' if location.lower() == location_finish[0].lower()\
                        and True in location_finish and 'bucuresti' != location.lower()\
                            else location,
                remote='on-site',
            ).to_dict())

        start_row_page += 10

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Systematic"
    logo_link = "https://stemo.bg/uploads/media/stemo_partners/0001/01/033c7005869e36d01af59bf2f777b3c9bf14569c.jpeg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
