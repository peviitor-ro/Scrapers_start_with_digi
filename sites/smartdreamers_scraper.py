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
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from SmartDreamers scraper.
    '''
    soup = GetStaticSoup("https://www.smartdreamers.com/careers#jobslisting")

    job_list = []
    count = 0

    jobs_not_repeat = [] # not repeat jobs
    if (links_to_jobs := soup.select('div.row-fluid a.hs-button')):
        for link_job in links_to_jobs:
            if 'career-page' in link_job['href']:

                # make second request
                soup2 = GetStaticSoup(link_job['href'])

                job_type = 'on-site'

                #
                city = None
                county = None
                #

                if (location := soup2.select_one('div.location-inline')):
                    location = location.text.strip().lower()
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
                job_list.append(Item(
                    job_title=soup2.select_one('div.headline').text.strip(),
                    job_link=link_job['href'],
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
