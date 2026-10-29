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
# Company ---> makita
# Link ------> https://makitajobs.ro/locuri-de-munca/
#
#
import base64
import re
import time
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def get_location(soup):
    '''
    ... extract the job location from the base64 encoded page content.
    '''
    for text_node in soup.find_all(string=re.compile('bunch_service_single')):
        match = re.search(r'text="([^"]+)"', str(text_node))
        if not match:
            continue

        encoded = match.group(1)
        decoded = base64.b64decode(encoded + '=' * (-len(encoded) % 4)).decode('utf-8', errors='replace')
        text = re.sub(r'<[^>]+>', ' ', decoded)

        address_match = re.search(r'Locul tău de muncă stabil\s*-\s*([^<]+)', text)
        if address_match:
            return address_match.group(1).strip().split(',')[-1].strip().split()[-1]

        county_match = re.search(r'Jud\.\s*([^\s<]+)', text)
        if county_match:
            return county_match.group(1).strip()

    return None


def scraper():
    '''
    ... scrape data from makita scraper.
    '''
    soup = GetStaticSoup("https://makitajobs.ro/locuri-de-munca/")

    job_list = []
    for job in soup.find_all('div', attrs={'class': 'box-right'}):
        link = "https://makitajobs.ro" + job.find('div', attrs={'class': 'content-button'}).find('a')['href']

        location = None
        for _ in range(3):
            try:
                location = get_location(GetStaticSoup(link))
                break
            except Exception:
                time.sleep(2)
                continue

        if location is None:
            continue

        location_finish = get_county(location=location)

        
        # get jobs items from response
        job_list.append(Item(
            job_title=job.find('div', attrs={'class': 'content-title'}).text,
            job_link=link,
            company='makita',
            country='România',
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

    company_name = "makita"
    logo_link = "https://www.makita.ro/data/pam/public/makita_logo3.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
