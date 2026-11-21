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
# Company ---> Evalueserve
# Link ------> https://www.evalueserve.com/jobs/
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
    ... scrape data from Evalueserve scraper.
    '''
    soup = GetStaticSoup("https://www.evalueserve.com/jobs/")

    job_list = []
    for job in soup.select('div[class*="db-job-title"]'):
        job = job.parent

        # get location
        location = job.select_one('div.db-location-country')
        location_parts = [part.strip() for part in location.get_text(strip=True).split(',')] if location else []

        city = location_parts[0] if location_parts else ''
        county = location_parts[1] if len(location_parts) > 2 else ''
        country = location_parts[-1] if location_parts else ''

        # get jobs items from response
        job_list.append(Item(
            job_title=job.select_one('div.db-job-title h4').text.strip(),
            job_link=job.select_one('div.db-job-link a')['href'],
            company='Evalueserve',
            country=country,
            county=county,
            city=city,
            remote='remote',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Evalueserve"
    logo_link = "https://mltfwbciccuo.i.optimole.com/w:985/h:101/q:mauto/https://www.evalueserve.com/wp-content/uploads/2021/10/Evalueserve__logo.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
