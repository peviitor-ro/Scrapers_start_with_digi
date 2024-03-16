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
# Company ---> SeedBlink
# Link ------> https://seedblink.com/careers
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
    ... scrape data from SeedBlink scraper.
    '''
    soup = GetStaticSoup("https://seedblink.com/careers")

    job_list = []
    for job in soup.select('div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-sm-6.MuiGrid-grid-md-4'):

        if (location := job.select_one('div.MuiCardContent-root').select('p')[1].text)\
                                and location.lower() == 'bucharest':
            location = 'Bucuresti'

        location_finish = get_county(location=location)

        # get jobs items from response
        job_list.append(Item(
            job_title=job.select_one('div.MuiCardContent-root').select('p')[0].text,
            job_link=f"https://seedblink.com{job.select_one('a')['href']}",
            company='SeedBlink',
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

    company_name = "SeedBlink"
    logo_link = "https://seedblink.com/_next/static/images/seedblink-logo-f8978e8317c9a57dca40e52a53247d6e.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
