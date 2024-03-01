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
# Company ---> Intersnack
# Link ------> https://www.intersnack.ro/cariere/oportunitati-de-cariera
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
    ... scrape data from Intersnack scraper.
    '''
    soup = GetStaticSoup("https://www.intersnack.ro/cariere/oportunitati-de-cariera")
    job_list = []
    for job in soup.select('div.ce__isnack-teaserpillar-teaser-item.bg__isnack.bg__isnack-red'):
        
        location = job.select_one('h3.text-center').text.strip()

        location_finish = get_county(location=location)

        # get jobs items from response
        job_list.append(Item(
            job_title=job.select_one('h2.text-center.font__is').text.strip(),
            job_link=f"https://www.intersnack.ro{job.select_one('a.btn.btn-ghost.btn-ghost-light')['href']}",
            company='Intersnack',
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

    company_name = "Intersnack"
    logo_link = "https://www.intersnack.ro/fileadmin/_processed_/8/0/csm_ins_with_Claim_ver_RGB_01_9352fb7970.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
