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
# Scrap new company ---> TheCoders
# Link ------> https://thecoders.ro/en/joburi/all/
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)


def get_jobs_from_page(page):
    '''
    ... collect jobs from a listing page.
    '''
    soup = GetStaticSoup(f"https://thecoders.ro/en/joburi/all/?page={page}")

    job_list = []
    for job in soup.find_all('div', class_='inner'):
        title_tag = job.find('a', class_='fancy red')
        link_tag = job.find('a', class_='button bg-blue white iblock fs-12 mb-30 fancy')
        tags_tag = job.find('li', class_='tags no-wrap pb-30')

        if title_tag is None or link_tag is None or tags_tag is None:
            continue

        tags_text = tags_tag.get_text(' ', strip=True)
        if tags_text == 'Closed':
            continue

        city = 'Romania'
        county = ''
        for location in ['Cluj Napoca', 'Cluj', 'Bucuresti', 'Bucharest', 'Iasi', 'Timisoara', 'Sibiu', 'Brasov']:
            if location.lower() in tags_text.lower():
                normalized_location = 'Cluj' if location.lower() == 'cluj napoca' else location
                normalized_location = 'Bucuresti' if normalized_location.lower() == 'bucharest' else normalized_location
                county_data = get_county(location=normalized_location)
                county = county_data[0] if True in county_data else ''
                city = location
                break

        job_list.append(Item(
            job_title=title_tag.get_text(strip=True),
            job_link=link_tag['data-href'],
            company='TheCoders',
            country='Romania',
            county=county,
            city=city,
            remote='hybrid' if 'hybrid' in tags_text.lower() else 'on-site',
        ).to_dict())

    return job_list


def scraper():
    '''
    ... scrape data from TheCoders scraper.
    '''
    page = 1
    job_list = []

    while True:
        jobs = get_jobs_from_page(page)
        if not jobs:
            break

        job_list.extend(jobs)
        page += 1

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "TheCoders"
    logo_link = "https://thecoders.ro/images/logo.png"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
