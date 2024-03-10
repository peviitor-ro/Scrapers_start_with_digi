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
# Company ---> RedBeeSoftware
# Link ------> https://redbeesoftware.com/job-openings/
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
    ... scrape data from RedBeeSoftware scraper.
    '''
    soup = GetStaticSoup("https://redbeesoftware.com/job-openings/")

    job_list = []
    for job in soup.select('div.elementor-widget-container'):

        if (button_learn_more := job.select_one('span.elementor-button-text')) is not None\
                                    and button_learn_more.text.lower() == 'learn more':

            # second request
            soup_2 = GetStaticSoup(job.select_one('a')['href'])      

            # get jobs items from response
            job_list.append(Item(
                job_title=soup_2.select_one('h1.elementor-heading-title.elementor-size-default').text.strip(),
                job_link=job.select_one('a')['href'],
                company='RedBeeSoftware',
                country='Romania',
                county='Cluj',
                city='Cluj-Napoca',
                remote='on-site',
            ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "RedBeeSoftware"
    logo_link = "https://redbeesoftware.com/wp-content/uploads/2022/07/Redbee-vertical-red@2x-1.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
