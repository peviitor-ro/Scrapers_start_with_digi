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
# Company ---> Idemia
# Link ------> https://careers.idemia.com/search/\?createNewAlert\=false\&q\=\&locationsearch\=Romania\&optionsFacetsDD_city\=\&optionsFacetsDD_customfield2\=\&optionsFacetsDD_customfield3\=
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
    ... scrape data from Idemia scraper.
    '''
    soup = GetStaticSoup("https://careers.idemia.com/search/?createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_city=&optionsFacetsDD_customfield2=&optionsFacetsDD_customfield3=")

    job_list = []
    for job in soup.select('tr.data-row'):
        
        if (location := job.select_one('span.jobLocation').text.strip().split(',')[0].lower()) == 'bucharest':
            location = 'Bucuresti'

        # if location are diferent: dakar ---> or something else.
        if location.lower != 'bucharest':
            location = 'Bucuresti'

        location_finish = get_county(location=location)

        # get jobs items from response
        job_list.append(Item(
            job_title=job.select_one('a.jobTitle-link').text,
            job_link=f"https://careers.idemia.com{job.select_one('a.jobTitle-link')['href']}",
            company='Idemia',
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

    company_name = "Idemia"
    logo_link = "https://www.nist.gov/sites/default/files/images/2022/07/20/IDEMIA.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
