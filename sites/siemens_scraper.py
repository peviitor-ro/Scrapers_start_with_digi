#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> Siemens
# Link ------> https://jobs.siemens.com/en_US/externaljobs/SearchJobs/?search=Romania
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
from bs4 import BeautifulSoup

from __utils.req_bs4_shorts import session
from __utils import (
    get_county,
    remove_diacritics,
    Item,
    UpdateAPI,
)


BASE_URL = 'https://jobs.siemens.com/en_US/externaljobs/SearchJobs/'
PAGE_SIZE = 6

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
}


def get_search_page(offset: int):
    '''
    ... return the soup object for one page of the Romania job search.
    '''

    url = f'{BASE_URL}?search=Romania&folderOffset={offset}'
    response = session.get(url, headers=HEADERS, verify=False, timeout=30)

    if response.status_code != 200:
        return None

    return BeautifulSoup(response.text, 'lxml')


def get_job_details(link: str):
    '''
    ... return (locations, work_mode) from a job detail page.
    '''

    response = session.get(link, headers=HEADERS, verify=False, timeout=30)
    if response.status_code != 200:
        return [], ''

    soup = BeautifulSoup(response.text, 'lxml')

    locations = [
        item.get_text(' ', strip=True)
        for item in soup.select('.tf_locations ul.list--locations li')
    ]

    work_mode = ''
    for field in soup.select('.article__content__view__field'):
        label = field.select_one('.article__content__view__field__label')
        if label and label.get_text(strip=True) == 'Work mode':
            value = field.select_one('.article__content__view__field__value')
            work_mode = value.get_text(' ', strip=True) if value else ''
            break

    return locations, work_mode


def get_remote(work_mode: str):
    '''
    ... map the site work mode to the value used by the scraper output.
    '''

    mode = work_mode.lower()
    if 'hybrid' in mode:
        return 'hybrid'
    if 'remote' in mode:
        return 'remote'
    return 'onsite'


def get_romanian_towns(locations):
    '''
    ... extract the Romanian cities from the job locations.
    '''

    towns = []
    for location in locations:
        parts = location.rsplit(' - ', 2)
        if len(parts) < 3 or parts[-1].strip().lower() != 'romania':
            continue

        city = remove_diacritics(parts[0].strip())
        if city.lower() in ('bucharest', 'bucuresti'):
            city = 'Bucuresti'
        else:
            city = city.title()

        if city and city not in towns:
            towns.append(city)

    return towns


def scraper():
    '''
    ... scrape data from Siemens scraper.
    '''

    job_list = []
    seen_links = set()
    offset = 0

    while True:
        soup = get_search_page(offset)
        if soup is None:
            break

        articles = soup.select('article.article--result')
        if not articles:
            break

        for article in articles:
            title_tag = article.select_one('h3.article__header__text__title a')
            if not title_tag:
                continue

            link = title_tag.get('href')
            if not link or link in seen_links:
                continue
            seen_links.add(link)

            job_title = title_tag.get_text(' ', strip=True)
            if not job_title:
                continue

            locations, work_mode = get_job_details(link)
            if not locations:
                location_tag = article.select_one('.list-item-location')
                locations = [location_tag.get_text(' ', strip=True)] if location_tag else []

            location_towns = get_romanian_towns(locations)
            if not location_towns:
                continue

            job_counties = [get_county(city) for city in location_towns]
            counties = [county if found else None for county, found in job_counties]

            job_list.append(Item(
                job_title=job_title,
                job_link=link,
                company='Siemens',
                country='Romania',
                county=None if any(county is None for county in counties) else (
                    counties[0] if len(counties) == 1 else counties
                ),
                city=location_towns[0] if len(location_towns) == 1 else location_towns,
                remote=get_remote(work_mode),
            ).to_dict())

        if len(articles) < PAGE_SIZE:
            break

        offset += PAGE_SIZE

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Siemens"
    logo_link = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRy4X0h4JCY_Ex39Rq7sl1kIf4yXaF6In_BxJjl24CHFg&s"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
