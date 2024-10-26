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
# Company ---> SAP
# Link ------> https://jobs.sap.com/search/?q=&locationsearch=Romania&startrow=0&scrollToTable=True
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
    ... scrape data from SAP scraper.
    '''
    soup = GetStaticSoup("https://jobs.sap.com/search/?q=&locationsearch=Romania&startrow=0&scrollToTable=True")

    # extrat numbers of jobs for requests without errors
    pagination_string = int(list(set([elem.text.strip() for elem in soup.select('span.paginationLabel')]))[0].split()[-1])

    job_list = []
    pages = 0
    while pages < pagination_string:

        new_request = GetStaticSoup(f"https://jobs.sap.com/search/?q=&locationsearch=Romania&startrow={str(pages)}&scrollToTable=True")

        for job in new_request.select('tr.data-row'):
            title_link = job.select_one('a.jobTitle-link')

            # get location from site
            if (location := job.select_one('span.jobLocation').text.strip().split(',')[0]) == 'Bucharest':
                location = 'Bucuresti'

            # get county from location gather from site
            location_finish = get_county(location=location)

            # get jobs items from response
            job_list.append(Item(
                job_title=title_link.text,
                job_link=f"https://jobs.sap.com{title_link['href']}",
                company='SAP',
                country='Romania',
                county=location_finish[0] if True in location_finish else None,
                city='all' if location.lower() == location_finish[0].lower()\
                        and True in location_finish and 'bucuresti' != location.lower()\
                            else location,
                remote='on-site',
            ).to_dict())

        pages += 25

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "SAP"
    logo_link = "https://logowik.com/content/uploads/images/467_sap.jpg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
