#
#
#  Basic for scraping data from static pages
#  ... project made by Andrei Cojocaru
#  LinkedIn: https://www.linkedin.com/in/andrei-cojocaru-985932204/
#  Github: https://github.com/andreireporter13
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
# Company ---> AECOM
# Link ------> https://aecom.jobs/rom/jobs/
#
from __utils import (
    GetRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from AECOM scraper.
    '''

    job_list = list()

    api_url = "https://prod-search-api.jobsyn.org/api/v1/solr/search"
    custom_headers = {
        'accept': 'application/json',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-origin': 'aecom.jobs'
    }

    # fetch first page to get total number of pages
    data_jobs_api = GetRequestJson(url=f"{api_url}?page=1&location=rom&num_items=10",
                                   custom_headers=custom_headers)

    total_pages = data_jobs_api.get('pagination', {}).get('total_pages', 1)

    # get all jobs (the API caps num_items at 10, so paginate)
    for page in range(1, total_pages + 1):
        if page > 1:
            data_jobs_api = GetRequestJson(url=f"{api_url}?page={page}&location=rom&num_items=10",
                                           custom_headers=custom_headers)

        for job in data_jobs_api.get('jobs'):
            slug_job    = job.get('title_slug')
            idx         = job.get('guid')

            location    = job.get('city_exact')

            # change Bucharest
            if location.lower() in ['bucharest']:
                location = "Bucuresti"

            location_finish = get_county(location=location)

            job_list.append(Item(
                job_title=job.get('title_exact'),
                job_link=f"https://aecom.jobs/bucharest-rom/{slug_job}/{idx}/job/",
                company='AECOM',
                country='Romania',
                county=location_finish[0] if True in location_finish else None,
                city='all' if location.lower() == location_finish[0].lower()\
                            and True in location_finish and 'bucuresti' != location.lower()\
                                else location,
                remote='hybrid',
            ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "AECOM"
    logo_link = "https://1000logos.net/wp-content/uploads/2021/12/AECOM-logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
