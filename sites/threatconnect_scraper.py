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
# Company ---> ThreatConnect
# Link ------> https://jobs.lever.co/threatconnect
#
#
from __utils import (
    GetStaticSoup,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from ThreatConnect scraper.
    '''
    soup = GetStaticSoup("https://jobs.lever.co/threatconnect")

    no_jobs_text = soup.get_text(' ', strip=True)
    if 'No job postings currently open' in no_jobs_text:
        return []

    job_list = []
    for job in soup.find_all('div', class_='posting'):
        title_tag = job.find('h5')
        link_tag = job.find('a', class_='posting-title')

        if title_tag is None or link_tag is None:
            continue

        job_list.append(Item(
            job_title=title_tag.get_text(strip=True),
            job_link=link_tag['href'],
            company='ThreatConnect',
            country='Romania',
            county='',
            city='Romania',
            remote='remote',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "ThreatConnect"
    logo_link = "https://lever-client-logos.s3.us-west-2.amazonaws.com/38d6dcb4-a016-4ba9-8ef1-6d5d80c6688c-1766163095536.png"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
