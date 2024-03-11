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
# Company ---> RestartEnergy
# Link ------> https://restartenergy.ro/cariere/
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
    ... scrape data from RestartEnergy scraper.
    '''
    soup = GetStaticSoup("https://restartenergy.ro/cariere/")

    job_list = []
    for job in soup.select('div.vc_tta-panel-heading'):

        # get jobs items from response
        job_list.append(Item(
            job_title=job.select_one('span.vc_tta-title-text').text,
            job_link=f"https://restartenergy.ro/cariere/{job.select_one('a')['href']}",
            company='RestartEnergy',
            country='Romania',
            county='Timis',
            city='Timisoara',
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "RestartEnergy"
    logo_link = "https://upload.wikimedia.org/wikipedia/commons/9/91/Restart-energy-logo-yellow.jpg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
