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
# Company ---> Crosswork
# Link ------> https://crosswork.sincron.biz/
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
    ... scrape data from Crosswork scraper.
    '''
    soup = GetStaticSoup("https://crosswork.sincron.biz/")

    job_list = []
    for job in soup.find_all('div', attrs={'class': 'col-md-9'}):
        location = job.find_all('p', attrs={'class': 'job-info'})[0].text.strip()
        title_job = job.find('a').text

        job_type = ''
        if 'remote' in title_job.lower():
            job_type = 'remote'
        elif 'hibrid' in title_job.lower():
            job_type = 'hybrid'
        else:
            job_type = 'on-site'

        # get jobs items from response
        job_list.append(Item(
            job_title=title_job,
            job_link=job.find('a')['href'],
            company='Crosswork',
            country='Romania',
            county=get_county(location),
            city=location,
            remote=job_type,
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Crosswork"
    logo_link = "https://crosswork.sincron.biz/images/routes/5023/logo-crosswork.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
