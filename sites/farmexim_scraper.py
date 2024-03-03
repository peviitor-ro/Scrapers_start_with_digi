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
# Company ---> Farmexim
# Link ------> https://www.farmexim.ro/posturi-vacante-26.html
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
    ... scrape data from Farmexim scraper.
    '''
    soup = GetStaticSoup("https://www.farmexim.ro/posturi-vacante-26.html")

    job_list = []
    for job in soup.select('div.service-block-desc'):
        title_link = job.select_one('a')
        location = [element for element in\
                    job.select_one('ul.list-inline').text.split('\n')\
                    if element.strip()][0].split()[-1]
        
        location_finish = get_county(location=location)

        # get jobs items from response
        job_list.append(Item(
            job_title=title_link.text,
            job_link=f"https://www.farmexim.ro{title_link['href']}",
            company='Farmexim',
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

    company_name = "Farmexim"
    logo_link = "https://farmexim.ro/templates/default/assets/img/Logo-farmexm-135x77.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
