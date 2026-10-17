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
# Link ------> https://redbeesoftware.com/career
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
    soup = GetStaticSoup("https://redbeesoftware.com/career")

    job_list = []
    for job in soup.select('#career_post_list a[href^="/career/"]'):

        job_link = f"https://redbeesoftware.com{job['href']}"

        # second request -> get the work regime (remote / on-site)
        soup_2 = GetStaticSoup(job_link)
        job_text = soup_2.get_text(" ", strip=True).lower()

        # get jobs items from response
        job_list.append(Item(
            job_title=job.select_one('h3').text.strip(),
            job_link=job_link,
            company='RedBeeSoftware',
            country='Romania',
            county='Cluj',
            city='Cluj-Napoca',
            remote='remote' if 'regim de lucru: remote' in job_text else 'on-site',
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
