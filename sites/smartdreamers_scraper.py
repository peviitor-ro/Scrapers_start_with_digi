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
# Company ---> SmartDreamers
# Link ------> https://www.smartdreamers.com/careers\#jobslisting
#
#
from urllib.parse import urljoin

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

# job pages are served only on this subdomain (www variant returns 404)
BASE_URL = "https://careers.smartdreamers.com"


def scraper():
    '''
    ... scrape data from SmartDreamers scraper.
    '''
    soup = GetStaticSoup("https://www.smartdreamers.com/careers#jobslisting")

    job_list = []
    count = 0

    jobs_not_repeat = [] # not repeat jobs
    if (links_to_jobs := soup.select('div.row-fluid a.hs-button.job-apply')):
        for link_job in links_to_jobs:

            # make second request
            job_link = urljoin(f"{BASE_URL}/", link_job.get('href', ''))
            if not job_link or job_link in jobs_not_repeat:
                continue
            jobs_not_repeat.append(job_link)

            soup2 = GetStaticSoup(job_link)

            job_type = 'on-site'

            #
            city = None
            county = None
            #

            # location now lives in the listing card; detail page keeps it as fallback
            card = link_job.find_parent(class_='row-fluid')
            location = card.select_one('.job-location') if card else None
            if location is None:
                location = soup2.select_one('div.location-inline')

            if location:
                location = location.text.strip().lower().split(',')[0].strip()
                if location == 'remote':
                    job_type = 'remote'
                    city = None
                    county = None
                else:
                    if location == 'targu mures':
                        location = 'Targu-Mures'
                    elif location == 'bucharest':
                        location = 'Bucuresti'

                    city = location
                    county = get_county(location=location)
            else:
                job_type = 'remote'

            # got to individual pages and select data
            if (headline := soup2.select_one('div.headline')):
                job_title = headline.text.strip()
            elif card and (headline := card.select_one('.job-title')):
                job_title = headline.text.strip()
            else:
                continue

            job_list.append(Item(
                job_title=job_title,
                job_link=job_link,
                    company='SmartDreamers',
                    country='Romania',
                    county=None if county == None else (county[0] if True in county else None),
                    city=city,
                    remote=job_type,
                ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "SmartDreamers"
    logo_link = "https://www.romanianstartups.com/wp-content/uploads/2015/06/smartdreamers-logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
