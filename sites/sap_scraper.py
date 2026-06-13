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
import requests

from __utils import (
    HackCloudFlare,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from SAP scraper.
    '''
    job_list = []
    startrow = 0

    while True:
        try:
            soup = HackCloudFlare(f"https://jobs.sap.com/search/?q=&locationsearch=Romania&startrow={startrow}&scrollToTable=True")
        except requests.exceptions.ConnectionError:
            break

        rows = soup.select('tr.data-row')
        if not rows:
            break

        for job in rows:
            title_link = job.select_one('a.jobTitle-link')
            if not title_link:
                continue

            location_elem = job.select_one('span.jobLocation')
            if not location_elem:
                continue

            location = location_elem.text.strip().split(',')[0]
            if location == 'Bucharest':
                location = 'Bucuresti'

            location_finish = get_county(location=location)

            job_list.append(Item(
                job_title=title_link.text.strip(),
                job_link=f"https://jobs.sap.com{title_link['href']}",
                company='SAP',
                country='Romania',
                county=location_finish[0] if True in location_finish else None,
                city='all' if location.lower() == location_finish[0].lower()
                        and True in location_finish and 'bucuresti' != location.lower()
                            else location,
                remote='on-site',
            ).to_dict())

        startrow += 25

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
