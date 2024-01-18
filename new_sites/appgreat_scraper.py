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
# Company ---> AppGreat
# Link ------> https://www.appgr8.com/careers/
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
    ... scrape data from AppGreat scraper.
    '''
    soup = GetStaticSoup("https://www.appgr8.com/careers/")

    job_list = []
    for job in soup.find_all('a'):
        if 'positions' in job['href']:
            soup_2 = GetStaticSoup(job['href'])

            text_with_location = soup_2.find_all('p')
            for item in text_with_location:
                if 'Bucharest' in item.text:

                    # get jobs items from response
                    job_list.append(Item(
                        job_title=soup_2.find('h4', attrs={'class': 'elementor-heading-title elementor-size-default'}).text,
                        job_link=job['href'],
                        company='AppGreat',
                        country='Romania',
                        county='Bucuresti',
                        city='Bucuresti',
                        remote='remote',
                    ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "AppGreat"
    logo_link = "https://clutchco-static.s3.amazonaws.com/s3fs-public/logos/52175d74be34bfe849aef98e4ed36c4a.jpeg?VersionId=n87OrsHNyLbgXOo4MoyU4abLU4uoEUaV"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
