#
#
# Config for static Get Method -> For Html format!
#
# Company ---> HTSS
# Link ------> https://htssgroup.eu/careers/
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
from urllib.parse import urljoin

from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from HTSS scraper.
    '''

    url = 'https://htssgroup.eu/careers/'
    soup = GetStaticSoup(url)

    job_list = []
    for job in soup.select('a.jobs__item'):
        title = job.select_one('p.jobs__item__title')
        if title is None:
            continue

        location = 'Bucuresti'
        location_finish = get_county(location=location)

        job_list.append(Item(
            job_title=title.get_text(strip=True),
            job_link=urljoin(url, job.get('href', '')),
            company='HTSS',
            country='Romania',
            county=location_finish[0] if True in location_finish else None,
            city=location,
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "HTSS"
    logo_link = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRysC7nnegm3c49Yi7xNjgY3W5JNTxJ3gtSEiBlMQpfLA&s"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
