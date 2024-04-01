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
# Company ---> Suvoda
# Link ------> https://boards.greenhouse.io/embed/job_board?for=suvoda&b=https%3A%2F%2Fwww.suvoda.com%2Fcareers%2Fjob-openings
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
    ... scrape data from Suvoda scraper.
    '''
    soup = GetStaticSoup("https://boards.greenhouse.io/embed/job_board?for=suvoda&b=https%3A%2F%2Fwww.suvoda.com%2Fcareers%2Fjob-openings")

    job_list = []
    for job in soup.select('div.opening'):
        #
        if (ro_location := job.select_one('span.location').text) and 'romania' in ro_location.lower():
            clean_city = ro_location.split(',')[0]
            #
            location_finish = get_county(location=clean_city)

            # get jobs items from response
            job_list.append(Item(
                job_title=job.select_one('a').text,
                job_link=job.select_one('a').get('href'),
                company='Suvoda',
                country='Romania',
                county=location_finish[0] if True in location_finish else None,
                city='all' if clean_city.lower() == location_finish[0].lower()\
                        and True in location_finish and 'bucuresti' != clean_city.lower()\
                            else clean_city,
                remote='on-site',
            ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Suvoda"
    logo_link = "logo_link"

    jobs = scraper()
    print(jobs, len(jobs))

    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
